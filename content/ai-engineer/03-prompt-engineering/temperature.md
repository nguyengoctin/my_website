---
title: "Temperature"
description: "Temperature is a parameter used in language models that controls the randomness of the generated text."
summary: "Temperature là một tham số được sử dụng trong các language models để kiểm soát tính ngẫu nhiên của văn bản được tạo ra."
slug: "temperature"
date: 2026-08-01
weight: 37
next: "/ai-engineer/03-prompt-engineering/external-memory/"
prev: "/ai-engineer/03-prompt-engineering/sampling-parameters/"
draft: false


tags:
  - Prompt Engineering
  - LLM

toc: true
math: false
mermaid: false
---

**Temperature is a parameter | used in language models | that controls the randomness | of the generated text.**  
*Temperature là một tham số | được sử dụng trong các language models | để kiểm soát tính ngẫu nhiên | của văn bản được tạo ra.*

**A higher temperature value (e.g., 1.0) | leads to more diverse | and unpredictable outputs, | as the model is more likely | to sample less probable words.**  
*Giá trị temperature cao hơn (ví dụ: 1.0) | dẫn đến các đầu ra | đa dạng và khó đoán hơn, | vì model có nhiều khả năng | lấy mẫu các từ ít xác suất hơn.*

**Conversely, a lower temperature value (e.g., 0.2) | yields more deterministic, | conservative outputs, | favoring the most likely words | according to the model's training data.**  
*Ngược lại, giá trị temperature thấp hơn (ví dụ: 0.2) | tạo ra các đầu ra | mang tính quyết định, bảo thủ hơn, | ưu tiên các từ có xác suất cao nhất | theo dữ liệu huấn luyện của model.*

**Essentially, it influences | the probability distribution | from which the next word | is selected.**  
*Về cơ bản, nó ảnh hưởng đến | phân phối xác suất | mà từ tiếp theo | được chọn từ đó.*

## Resources

- [What Temperature Means in Natural Language Processing and AI](https://thenewstack.io/what-temperature-means-in-natural-language-processing-and-ai/) (article)
- [What is LLM Temperature? - IBM](https://www.ibm.com/think/topics/llm-temperature) (article)
- [How Temperature Settings Transform Your AI Agent's Responses](https://docsbot.ai/article/how-temperature-settings-transform-your-ai-agents-responses) (article)

## References

- https://roadmap.sh/ai-engineer (Node: Temperature)

---

[← Sampling Parameters](/ai-engineer/03-prompt-engineering/sampling-parameters/) · [AI Engineer Roadmap](/ai-engineer/) · [External Memory →](/ai-engineer/03-prompt-engineering/external-memory/)
