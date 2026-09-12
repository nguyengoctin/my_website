---
title: "Django production: best practice theo evidence cho backend API"
date: 2026-09-09T21:01:00+07:00
aliases:
  - django-production-best-practices
  - django-backend-best-practices
tags:
  - django
  - backend
  - drf
  - postgresql
  - celery
  - security
---

> [!TLDR]
> Với Django production, ưu tiên correctness và failure mode thật: database integrity → transaction → authorization → security → query behavior → migration → background jobs → observability. Những quy tắc như “phải có `services.py`”, “fat model/thin view” hay “luôn dùng ViewSet” chỉ nên xem là convention hoặc lựa chọn kiến trúc theo context.

## Context áp dụng

Note này được chắt lọc từ research về best practice Django cho một backend API có stack gần với project hiện tại:

- Django 5.1.
- Django REST Framework.
- PostgreSQL.
- Redis.
- Celery.
- SimpleJWT.
- Docker.
- Cloudflare Tunnel/reverse proxy.
- Cloudflare R2 cho media/object storage.

Mức rủi ro cần quan tâm không chỉ là code style mà còn gồm:

- authorization sai dẫn tới lộ dữ liệu;
- race condition khi nhiều request cùng ghi;
- task chạy trước khi transaction commit;
- N+1 query;
- migration gây lock production;
- upload không được giới hạn;
- reverse proxy/HTTPS config sai;
- dependency đã hết security support.

## Cách phân loại practice

| Mức | Ý nghĩa |
|---|---|
| **Requirement / baseline** | Không làm có failure mode rõ về security, correctness hoặc support. |
| **Established good practice** | Có maintainer guidance và rationale kỹ thuật mạnh; nên là mặc định. |
| **Context-dependent** | Tốt với workload/architecture phù hợp; áp dụng máy móc có thể làm hệ thống tệ hơn. |
| **Preference / convention** | Chủ yếu phục vụ consistency/readability; không đủ cơ sở để gọi là universal best practice. |

Mental model quan trọng:

```text
"popular" ≠ "best practice"
"vendor recommends" ≠ "best in every context"
"clean-looking architecture" ≠ "correct production system"
```

Đặc biệt với performance, phải đo workload thật trước khi tối ưu. Một rule như “field nào filter cũng phải index” hoặc “luôn dùng `.exists()`” không đáng tin nếu tách khỏi query plan và usage pattern thực tế.

## Decision về phiên bản Django

Research tại thời điểm 2026-09-09 cho thấy:

- Django 5.1 đã hết support từ 2025-12-03.
- Django 5.2 là nhánh LTS, research trước đó ghi nhận 5.2.17 và thời hạn support đến tháng 4/2028.
- Django 6.1.1 là release mới hơn tại thời điểm research.
- DRF 3.18 hỗ trợ Django 5.2, 6.0 và 6.1.
- Metadata SimpleJWT tại thời điểm research ghi support đến Django 6.0; việc chưa ghi 6.1 không tự động chứng minh rằng nó không chạy trên 6.1.

### Recommendation cho project hiện tại

Ưu tiên:

```text
Django 5.1
   ↓
Django 5.2 LTS
```

thay vì nhảy thẳng lên 6.1 chỉ vì đó là bản mới nhất.

Lý do:

- quay lại supported branch;
- giảm dependency compatibility risk;
- ít migration/churn hơn;
- LTS phù hợp production khi không cần feature mới của 6.x.

Decision này cần xem xét lại khi:

- project thực sự cần feature chỉ có ở Django 6.x;
- toàn bộ dependency đã xác nhận compatibility;
- test suite đủ mạnh để validate upgrade;
- có lý do vận hành đủ lớn để bỏ LTS.

## Security baseline trước khi bàn về architecture

Các cấu hình sau là production baseline, không phải style preference:

- `DEBUG=False`;
- `SECRET_KEY` không commit vào repository;
- `ALLOWED_HOSTS` giới hạn đúng host;
- HTTPS cho toàn bộ production traffic;
- không dùng `runserver` làm production server;
- database và Redis không expose trực tiếp ra Internet;
- có logging/error monitoring;
- có backup database và phải biết restore;
- chạy deployment checks của Django.

Verification đáng giữ:

```bash
python manage.py check --deploy
```

Lệnh này không chứng minh hệ thống hoàn toàn an toàn, nhưng giúp phát hiện nhiều deployment setting nguy hiểm hoặc thiếu sót.

### Reverse proxy và `SECURE_PROXY_SSL_HEADER`

Config kiểu:

```python
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
```

không được copy-paste mù quáng.

Chỉ nên bật khi:

1. request thực sự đi qua proxy đáng tin cậy;
2. proxy tự thiết lập header HTTPS;
3. proxy loại bỏ hoặc overwrite giá trị header do client tự gửi.

Nếu trust boundary này sai, Django có thể hiểu request HTTP là HTTPS.

Với Cloudflare Tunnel/reverse proxy, phải xác minh behavior của ingress/proxy trước khi coi dòng config trên là đúng.

## HTTPS, cookie, CSRF và CORS

Khi production chỉ chạy HTTPS và sử dụng cookie/session:

```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

là security practice đáng áp dụng.

HSTS hữu ích nhưng cần triển khai thận trọng. Các option như include-subdomains hoặc preload có hậu quả dài hạn, không nên bật chỉ vì “security checklist bảo vậy”.

### Không dùng `@csrf_exempt` để chữa triệu chứng

Anti-pattern:

```python
@csrf_exempt
```

chỉ để request hết báo lỗi CSRF.

Cần phân biệt:

```text
CORS
= browser có được phép gọi origin khác hay không

CSRF
= server có đang chấp nhận request dùng credential của user
  mà không có bằng chứng request được user chủ động tạo hay không
```

Fix CORS không đồng nghĩa fix CSRF và ngược lại.

### `CSRF_COOKIE_HTTPONLY=True` không phải universal security rule

Research trước đó ghi nhận chính Django xem option này chỉ đem lại ít practical protection trong nhiều trường hợp. Có thể cần vì audit/policy cụ thể, nhưng không nên gọi nó là best practice bắt buộc.

## Authentication không thay thế authorization

Trong DRF:

```text
Authentication
→ Ai đang gửi request?

Permission / Authorization
→ Người đó có được phép làm việc này không?
```

Một endpoint có:

```python
permission_classes = [IsAuthenticated]
```

vẫn có thể lộ dữ liệu nếu queryset không scope theo user/tenant.

Ví dụ cần audit:

```python
Order.objects.filter(user=request.user)
```

hoặc một cơ chế authorization tương đương.

### Failure mode quan trọng: object-level permission và list endpoint

Object-level permission không có nghĩa mọi object trong một list queryset tự động được filter an toàn.

Do đó:

```text
Queryset scope
+
permission check
```

phải được thiết kế cùng nhau.

Đây là một trong những điểm nên ưu tiên cao nhất khi audit API order/cart/profile hoặc bất kỳ dữ liệu user-owned nào.

## JWT là lựa chọn kiến trúc, không phải “Django best practice”

JWT hợp lý khi backend phục vụ:

- mobile app;
- Zalo Mini App;
- API client;
- frontend/backend tách biệt;
- service-to-service.

Nhưng câu:

```text
"REST API thì nên dùng JWT"
```

không phải universal rule.

First-party browser app có thể đơn giản hơn với Django session auth vì session lifecycle, logout và revocation đã có semantics phù hợp.

Với Mini App → Django API, bearer token/JWT là lựa chọn hợp lý do architecture, không phải vì JWT “modern hơn”.

## Database là lớp phòng thủ cuối cho invariant

Business validation ở serializer hoặc form rất hữu ích để tạo error message dễ hiểu, nhưng không đủ để đảm bảo correctness dưới concurrency.

Ví dụ invariant:

```text
Một user chỉ được có một active cart.
```

Code kiểu:

```python
if not Cart.objects.filter(...).exists():
    Cart.objects.create(...)
```

vẫn có race condition khi hai request chạy đồng thời.

Nếu invariant có thể biểu diễn ở database, ưu tiên constraint như:

```python
UniqueConstraint(...)
CheckConstraint(...)
```

Mental model:

```text
Serializer/form validation
→ UX và validation sớm

Database constraint
→ correctness cuối cùng, kể cả dưới concurrency
```

Đây là established good practice mạnh hơn việc cố giữ mọi rule trong Python.

## Transaction boundary phải theo business operation

Một flow như:

```text
create order
→ create order items
→ decrement stock
→ create payment record
```

nên có transaction boundary theo toàn bộ business operation.

Dùng explicit transaction:

```python
from django.db import transaction

with transaction.atomic():
    ...
```

thay vì wrap mọi request chỉ vì tiện.

### Vì sao không mặc định `ATOMIC_REQUESTS=True`

`ATOMIC_REQUESTS=True` wrap mỗi request trong transaction.

Trade-off:

- dễ reasoning cho write request đơn giản;
- nhưng tạo transaction overhead cho cả request;
- giữ transaction mở lâu hơn;
- có thể giảm throughput khi traffic tăng.

Với backend này, ưu tiên explicit `atomic()` tại operation thực sự cần atomicity.

## Không catch database error sai bên trong `atomic()`

Pattern cần tránh:

```python
with transaction.atomic():
    try:
        save_something()
    except IntegrityError:
        ...
```

Sau database error, transaction có thể ở trạng thái broken cho tới rollback.

Thực tế nên đặt exception boundary phù hợp bên ngoài transaction hoặc dùng nested `atomic()` khi cần một savepoint riêng.

Điểm cần nhớ không phải syntax cụ thể mà là:

> Sau database error, đừng giả định transaction hiện tại vẫn dùng bình thường.

## Concurrency: chọn đúng công cụ

### `F()` cho atomic update đơn giản

Code dễ bị lost update:

```python
product.stock -= 1
product.save()
```

Hai worker cùng đọc `stock=10` có thể cùng ghi `9`, trong khi kết quả đúng phải là `8`.

Với arithmetic update đơn giản:

```python
from django.db.models import F

Product.objects.filter(...).update(
    stock=F("stock") - 1
)
```

cho database thực hiện update dựa trên giá trị hiện tại.

### `select_for_update()` cho read → decision → write

Khi phải đọc row, kiểm tra state rồi mới quyết định write:

```python
from django.db import transaction

with transaction.atomic():
    order = (
        Order.objects
        .select_for_update()
        .get(...)
    )
    ...
```

`select_for_update()` lock row tới khi transaction kết thúc.

Không nên dùng khắp nơi vì lock có cost:

- giảm concurrency;
- tăng waiting;
- có thể tạo deadlock/contention.

Chỉ dùng khi invariant thực sự đòi serialization.

## Celery phải tôn trọng transaction boundary

Anti-pattern:

```python
order = Order.objects.create(...)
send_order.delay(order.id)
```

nếu code đang nằm trong một transaction chưa commit.

Worker có thể chạy trước commit và:

- không tìm thấy `Order`;
- đọc state cũ;
- thực hiện side effect dù transaction cuối cùng rollback.

Dùng:

```python
from django.db import transaction

transaction.on_commit(
    lambda: send_order.delay(order.id)
)
```

Mental model:

```text
DB transaction thành công
        ↓
commit
        ↓
enqueue Celery task
```

chứ không phải:

```text
enqueue task
        ↓
hy vọng database commit kịp
```

## Celery task quan trọng phải idempotent

Background task có thể được redeliver hoặc chạy lại trong failure scenario.

Do đó task nên chịu được retry khi có thể.

Ví dụ tác động thấp:

```text
send_email(order_id)
```

có thể chấp nhận duplicate hoặc dedupe.

Ví dụ tác động cao:

```text
charge_credit_card(order_id)
```

không được phép charge hai lần.

Các operation có side effect tài chính hoặc state quan trọng cần idempotency strategy như:

- idempotency key;
- unique constraint;
- state transition kiểm tra rõ;
- deduplication record.

Không giả định queue delivery đồng nghĩa business operation chạy chính xác một lần.

## Django Tasks không tự thay thế Celery

Django 6.x đã có Tasks framework trong core, nhưng nó cung cấp API/contract cho task chứ không tự biến Django thành production distributed queue.

Nếu project hiện tại đã dùng:

```text
Redis + Celery
```

và nó giải quyết đúng nhu cầu, không nên refactor chỉ vì Django có Tasks API mới.

Đây là ví dụ điển hình của:

```text
new feature ≠ reason to rewrite working infrastructure
```

## Query performance: ưu tiên N+1 trước micro-optimization

DRF serializer rất dễ tạo N+1 khi traverse relationship.

Ví dụ:

```python
orders = Order.objects.all()

for order in orders:
    print(order.customer.name)
```

có thể thành:

```text
1 query lấy orders
+
N query lấy customer
```

Công cụ thường dùng:

```python
select_related(...)
prefetch_related(...)
```

Nhưng không nên add relation preload hàng loạt nếu endpoint không cần.

Workflow đúng:

```text
đo query count
→ xác định N+1 thật
→ thêm select_related/prefetch_related
→ đo lại
```

DRF serializer không tự optimize queryset giúp mình.

## Index phải dựa trên workload và query plan

Rule:

```text
"field nào filter cũng index"
```

là cargo cult nếu dùng như luật.

Index có cost:

- tăng disk;
- làm insert/update/delete tốn hơn;
- PostgreSQL phải maintain;
- query planner có thể không dùng.

Candidate thường đáng xem xét là field xuất hiện nhiều trong:

```text
WHERE
JOIN
ORDER BY
```

nhưng decision nên dựa vào query thật.

Dùng:

```python
queryset.explain()
```

để xem query plan khi cần.

Mental model:

```text
profile
→ inspect query
→ inspect plan
→ change
→ measure again
```

## `.exists()` và `.count()` không phải lúc nào cũng “tối ưu”

Nếu chỉ cần boolean:

```python
qs.exists()
```

thường hợp lý.

Nhưng:

```python
if qs.exists():
    for item in qs:
        ...
```

có thể tạo hai query thay vì chỉ evaluate queryset một lần.

Tương tự với `.count()`.

Không học ORM optimization dưới dạng rule:

```text
"always use exists()"
```

mà phải nhìn vào lifecycle của queryset.

## Pagination cho collection không bounded

Endpoint kiểu:

```http
GET /orders
```

không nên trả vô hạn khi dữ liệu tăng.

Failure mode:

- query time tăng;
- RAM tăng;
- serialization cost tăng;
- payload lớn;
- client render chậm.

Generic views/ViewSet của DRF hỗ trợ pagination mechanism, nhưng custom `APIView` không tự paginate nếu mình không implement.

## DRF throttling không phải DDoS protection

DRF throttling phù hợp để:

- giới hạn usage;
- business policy;
- basic abuse control.

Không nên coi nó là lớp bảo vệ DDoS hoặc brute-force hoàn chỉnh.

Với architecture có Cloudflare:

```text
Internet
   ↓
Cloudflare / edge rate limit / WAF
   ↓
Django / DRF throttle
   ↓
application
```

Edge nên chịu phần lớn volumetric/abuse protection; DRF throttle là policy layer bổ sung.

## Migration: local thành công không chứng minh production an toàn

Migration nhanh trên laptop không nói nhiều về behavior trên table lớn production.

### Data migration phải dùng historical model

Trong migration, ưu tiên:

```python
apps.get_model(...)
```

thay vì:

```python
from orders.models import Order
```

Import model hiện tại có thể khiến migration cũ hỏng sau khi model evolve.

### Table lớn và index

PostgreSQL có concurrent index creation và Django hỗ trợ operation như:

```python
AddIndexConcurrently
```

để giảm blocking write so với index creation thông thường.

Đây chỉ trở thành ưu tiên cao khi table đủ lớn và downtime/lock có ý nghĩa.

### Data migration lớn

Có thể cần:

- batching;
- non-atomic strategy;
- tách schema migration và data backfill;
- verification theo từng bước.

Không áp dụng phức tạp này cho table nhỏ chỉ vì “zero-downtime best practice”.

## Upload: giới hạn ở nhiều lớp

User upload là untrusted input.

Chỉ dựa vào Django upload settings không đủ cho request rất lớn.

Với stack dùng Cloudflare và R2, mental model tốt hơn:

```text
Internet
   ↓
Cloudflare / proxy request-size limit
   ↓
Django authorization + validation
   ↓
R2 object storage
```

Không nên để media lớn sống trong container Django nếu object storage đã là architecture target.

## Redis/cache: chỉ cache sau khi có lý do đo được

Redis có thể giúp nhưng cache thêm:

- stale data;
- invalidation logic;
- memory cost;
- dependency vận hành;
- nguy cơ leak dữ liệu giữa user/tenant nếu cache key sai.

Anti-pattern:

```text
"Có Redis rồi thì cache API"
```

Đặc biệt với response phụ thuộc user, cache key phải encode đủ authorization scope.

Caching là context-dependent optimization, không phải default correctness layer.

## Signals: tránh giấu core workflow

Signals tạo loose coupling ở bề mặt nhưng dễ làm execution flow khó lần theo.

Core business flow kiểu:

```text
Order created
→ decrement stock
→ create payment
→ enqueue receipt
```

không nên bị giấu thành:

```text
post_save
→ signal A
→ signal B
→ task C
```

Signals hợp hơn với event thực sự cross-cutting hoặc extension-like, nhưng ngay cả vậy explicit call thường dễ debug hơn khi sender/receiver đều nằm trong cùng project.

## Service layer là công cụ, không phải luật

Cấu trúc như:

```text
services.py
selectors.py
```

có thể hữu ích, nhưng không phải requirement của Django.

Service/use-case layer đáng xuất hiện khi operation:

```text
span nhiều model
+ transaction
+ external API
+ Celery
+ được gọi từ API/admin/task
```

Ví dụ:

```python
place_order(...)
cancel_order(...)
confirm_payment(...)
```

thường có cohesion tốt ở use-case/service boundary.

Không cần bọc CRUD đơn giản:

```python
get_product_by_id()
create_category()
update_customer_name()
```

chỉ để project “clean”.

### Architecture recommendation cho project này

```text
DRF view
    ↓
HTTP concern + permission orchestration

Serializer
    ↓
parsing + API validation

Explicit service/use-case
    ↓
chỉ khi business operation đủ phức tạp

Models / QuerySets
    ↓
data behavior và query composition

PostgreSQL constraints
    ↓
final integrity boundary

transaction.on_commit()
    ↓
Celery
    ↓
slow/external side effects
```

Không ép mọi request phải đi qua đủ mọi layer.

CRUD đơn giản có thể:

```text
view/serializer
→ model/queryset
```

Workflow như đặt món, tồn kho, thanh toán hoặc hoàn tiền mới đáng có explicit use-case boundary.

## “Fat models, thin views” chỉ là heuristic

Method như:

```python
order.cancel()
```

rất hợp nếu behavior chủ yếu thuộc `Order`.

Nhưng nếu `cancel()` phải:

```text
refund payment provider
→ restore stock
→ release voucher
→ notify user
→ write audit event
```

thì model dễ biến thành god object.

Rule nên giữ:

> Đặt business logic ở nơi có cohesion tốt nhất và dependency rõ nhất, không theo khẩu hiệu “mọi logic phải ở model” hoặc “mọi logic phải ở service”.

## ViewSet, generic view và APIView

Không có winner universal.

| Tool | Phù hợp |
|---|---|
| `ModelViewSet` | CRUD resource khá chuẩn |
| Generic views | CRUD nhưng muốn explicit hơn |
| `APIView` | Workflow/custom endpoint |
| Function-based view | Endpoint nhỏ và đơn giản |

Đây là architecture/convention choice. Đừng refactor chỉ để thống nhất theo một trường phái nếu current behavior rõ và maintainable.

## Serializer không phải domain layer

Serializer phù hợp với:

```text
parse request
type validation
input validation
representation
API-specific error
```

Nếu `Serializer.create()` dần chứa:

```text
transaction
inventory
payment gateway
voucher
Celery
notification
analytics
```

thì use case đã vượt khỏi serialization concern.

Khi đó explicit domain/service operation giúp reuse và test tốt hơn.

Không cần extract serializer CRUD ngắn chỉ vì styleguide bảo vậy.

## Custom User: quyết định phụ thuộc lifecycle

Cho project mới, custom user từ đầu thường đáng làm, thường bằng `AbstractUser`, vì đổi user model sau này phức tạp.

Nhưng với project đã production ổn bằng default User:

```text
"đổi sang custom user để theo best practice"
```

không phải lý do đủ mạnh.

Lifecycle quyết định recommendation.

## `null=True` trên `CharField` không phải security rule

Tránh cả:

```text
NULL
""
```

cùng biểu diễn “không có dữ liệu” thường giúp model nhất quán.

Nhưng đây chủ yếu là data-model convention và có ngoại lệ hợp lệ. Không nên biến thành lint rule tuyệt đối.

## Async Django: dùng khi workload thật sự cần

Async hữu ích với nhiều concurrent I/O như:

```text
external API calls
streaming
long polling
websocket-related workload
```

Nhưng:

```text
async ≠ ORM tự nhanh hơn
```

và transaction-sensitive code vẫn cần cân nhắc sync boundary theo support của Django.

Đổi toàn bộ views sang `async def` chỉ vì “async nhanh hơn” là anti-pattern.

## Testing: test failure mode, không chase coverage %

Ưu tiên test:

- business invariant;
- permission và ownership;
- transaction quan trọng;
- Celery idempotency;
- migration có rủi ro;
- query count/N+1 ở endpoint quan trọng.

Không có lý do kỹ thuật chung để ép 100% coverage.

### Transaction/concurrency test

`TestCase` phù hợp phần lớn test vì nhanh.

Nhưng behavior như `select_for_update()` cần test đúng transaction semantics; `TransactionTestCase` phù hợp hơn cho các scenario này.

Với PostgreSQL-specific behavior như:

- locking;
- constraint;
- query planner;
- PostgreSQL migration operation;

test quan trọng nên chạy trên PostgreSQL thật thay vì giả định SQLite tương đương.

## Observability là production requirement, structured logging chỉ là implementation choice

Production backend phải giúp trả lời:

```text
request nào lỗi?
endpoint nào chậm?
query nào chậm?
Celery task nào fail?
deployment nào bắt đầu regression?
```

Nên có khả năng correlate:

```text
request ID
task ID
status
latency
important domain event
```

Không log secret hoặc credential:

```text
Authorization header
password
token
secret
raw sensitive payload
```

Structured logging là preference/implementation detail; khả năng debug production là established good practice.

## Anti-pattern và advice lỗi thời cần tránh

| Advice | Đánh giá |
|---|---|
| Mỗi model phải có service | Cargo cult |
| Mọi business logic phải ở model | Heuristic bị áp dụng quá mức |
| Mọi business logic phải ra service | Heuristic bị áp dụng quá mức |
| Luôn dùng ViewSet | Convention |
| Luôn dùng APIView | Convention |
| Phải có `selectors.py` | Convention |
| Luôn có repository layer trên Django ORM | Context-dependent |
| Settings bắt buộc phải tách `base/dev/prod.py` | Convention |
| `.env` tự nó là secret-management best practice | Sai abstraction |
| UUID luôn tốt hơn integer PK | Context-dependent |
| Soft delete luôn tốt hơn hard delete | Domain-dependent |
| Có Redis thì nên cache mọi thứ | Cargo cult |
| Async luôn nhanh hơn sync | Sai |
| Field nào filter cũng cần index | Cargo cult |
| `.exists()` luôn nhanh hơn | Context-dependent |
| Signals luôn giúp decouple | Thường làm flow khó trace |
| `ATOMIC_REQUESTS=True` luôn tốt | Context-dependent |
| JWT luôn tốt hơn session | Architecture-dependent |
| DRF throttle chống DDoS | Sai |
| Serializer validation đủ bảo vệ invariant | Sai dưới concurrency |
| Latest Django luôn là production choice tốt nhất | Sai |

## Khi nào recommendation cần đổi

| Context | Điều cần xem lại |
|---|---|
| Internal CRUD tool ít user | Có thể đơn giản hóa migration, cache, observability |
| Table lớn / traffic cao | Online migration, index strategy, pooling trở nên quan trọng |
| First-party browser app | Session auth có thể tốt hơn JWT |
| Mobile/Mini App/API ecosystem | Bearer/JWT hợp lý hơn |
| Không có concurrent writes | Locking có thể không cần |
| Heavy external I/O | Async/ASGI đáng cân nhắc hơn |
| Project mới | Custom User từ đầu đáng làm |
| Project production lâu năm | Không đổi user architecture chỉ vì convention |
| Không có background job | Celery có thể là complexity không cần thiết |
| Upload file lớn | Direct-to-object-storage càng đáng cân nhắc |
| Cần feature Django 6.x | Upgrade sau dependency/test validation |
| Ưu tiên stability | Django 5.2 LTS là target hợp lý hơn cho project 5.1 hiện tại |

## Checklist audit thực tế cho backend hiện tại

Thứ tự này ưu tiên failure mode nghiêm trọng trước code cleanliness.

### 1. Version

- Nâng Django 5.1 → 5.2 LTS.
- Kiểm tra compatibility của DRF, SimpleJWT và package liên quan.
- Chạy full test và migration verification.

### 2. Production security

Kiểm tra:

```text
DEBUG
SECRET_KEY
ALLOWED_HOSTS
HTTPS
proxy headers
CORS
CSRF
secure cookies
database exposure
Redis exposure
```

Sau đó:

```bash
python manage.py check --deploy
```

### 3. Authorization

Audit mọi endpoint dữ liệu user-owned:

```text
orders
cart
profile
address
voucher
payment-related object
```

Xác minh queryset scope và object authorization, không chỉ nhìn `IsAuthenticated`.

### 4. Data integrity và concurrency

Tìm invariant hiện chỉ được giữ bằng Python.

Xem xét:

```text
UniqueConstraint
CheckConstraint
F()
transaction.atomic()
select_for_update()
```

chỉ ở nơi failure mode thật sự tồn tại.

### 5. Celery boundary

Xác minh:

```text
task enqueue sau commit
task quan trọng idempotent
core workflow không bị giấu trong signal chain
```

### 6. Query behavior

Đo:

```text
query count
N+1
slow query
query plan
```

rồi mới quyết định:

```text
select_related
prefetch_related
index
cache
```

### 7. Migration và upload

Kiểm tra:

- data migration dùng historical model;
- migration trên table lớn có lock risk;
- request/upload size được giới hạn ở proxy lẫn app;
- media phù hợp được đưa ra object storage như R2.

### 8. Architecture refactor

Chỉ sau correctness/security/performance audit mới quyết định có cần:

```text
service/use-case layer
selector
custom abstraction
```

Không refactor project để “trông giống styleguide” nếu chưa giải quyết failure mode thực tế.

## Mental model cuối cùng

Có thể dùng thứ tự sau khi review một Django backend:

```text
1. Version còn support không?
          ↓
2. Request có được authenticate + authorize đúng không?
          ↓
3. Database có giữ invariant khi concurrent không?
          ↓
4. Transaction boundary đúng business operation không?
          ↓
5. Side effect/task có chạy đúng sau commit và chịu retry không?
          ↓
6. Query có scale không?
          ↓
7. Migration/deploy có an toàn không?
          ↓
8. Có đủ observability để debug production không?
          ↓
9. Sau đó mới tối ưu architecture/style.
```

Đây là thứ tự đáng giữ hơn bất kỳ “Django folder structure chuẩn” nào.

## References

Các nguồn dưới đây đã được dùng trong research trước đó và đáng giữ để kiểm chứng lại theo version.

- Django downloads / supported versions: https://www.djangoproject.com/download/
- Django deployment checklist: https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/
- Django security: https://docs.djangoproject.com/en/6.0/topics/security/
- Django CSRF: https://docs.djangoproject.com/en/6.0/ref/csrf/
- Django settings: https://docs.djangoproject.com/en/6.0/ref/settings/
- Django database optimization: https://docs.djangoproject.com/en/6.0/topics/db/optimization/
- Django transactions: https://docs.djangoproject.com/en/6.0/topics/db/transactions/
- Django constraints: https://docs.djangoproject.com/en/6.0/ref/models/constraints/
- Django expressions / `F()`: https://docs.djangoproject.com/en/6.0/ref/models/expressions/
- Django QuerySet API / `select_for_update()`: https://docs.djangoproject.com/en/6.0/ref/models/querysets/
- Django migrations: https://docs.djangoproject.com/en/6.0/topics/migrations/
- Writing Django migrations: https://docs.djangoproject.com/en/6.0/howto/writing-migrations/
- PostgreSQL-specific migration operations: https://docs.djangoproject.com/en/6.0/ref/contrib/postgres/operations/
- Django signals: https://docs.djangoproject.com/en/6.0/topics/signals/
- Django async support: https://docs.djangoproject.com/en/6.0/topics/async/
- Django testing overview: https://docs.djangoproject.com/en/6.0/topics/testing/overview/
- Django custom user model: https://docs.djangoproject.com/en/6.0/topics/auth/customizing/
- Django model fields: https://docs.djangoproject.com/en/5.2/ref/models/fields/
- Django Tasks framework: https://docs.djangoproject.com/en/6.0/ref/tasks/
- DRF authentication: https://www.django-rest-framework.org/api-guide/authentication/
- DRF permissions: https://www.django-rest-framework.org/api-guide/permissions/
- DRF generic views and N+1 guidance: https://www.django-rest-framework.org/api-guide/generic-views/
- DRF pagination: https://www.django-rest-framework.org/api-guide/pagination/
- DRF throttling: https://www.django-rest-framework.org/api-guide/throttling/
- DRF project / compatibility: https://www.django-rest-framework.org/
- Celery task guidance: https://docs.celeryq.dev/en/stable/userguide/tasks.html
