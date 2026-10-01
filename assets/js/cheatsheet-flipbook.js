document.addEventListener("DOMContentLoaded", async function () {
    const workspace = document.querySelector(".cheatsheet-single") || document.querySelector("#flipbook-wrapper"); const pdfUrl = workspace ? workspace.getAttribute("data-pdf-url") : null;
    if (!pdfUrl) return;

    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

    const wrapper = document.getElementById('flipbook-wrapper');
    const container = document.getElementById('flipbook-container');
    const skeleton = document.getElementById('skeleton-loader');
    
    const pageIndicator = document.getElementById('dock-page-indicator');
    const pageIndicatorMobile = document.getElementById('dock-page-indicator-mobile');
    
    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    const btnPrevMobile = document.getElementById('btn-prev-mobile');
    const btnNextMobile = document.getElementById('btn-next-mobile');
    
    const btnZoomPage = document.getElementById('btn-zoom-page');

    // Smart Zoom Overlay Elements
    const zoomOverlay = document.getElementById('smart-zoom-overlay');
    const zoomStage = document.getElementById('zoom-stage-container');
    const zoomCanvas = document.getElementById('smart-zoom-canvas');
    const zoomPageTitle = document.getElementById('zoom-page-title');
    const zoomLevelText = document.getElementById('zoom-level-text');
    
    const btnZoomIn = document.getElementById('btn-zoom-in-overlay');
    const btnZoomOut = document.getElementById('btn-zoom-out-overlay');
    const btnZoomReset = document.getElementById('btn-zoom-reset-overlay');
    const btnZoomClose = document.getElementById('btn-zoom-close-overlay');
    const btnZoomPrev = document.getElementById('btn-zoom-prev-overlay');
    const btnZoomNext = document.getElementById('btn-zoom-next-overlay');

    let pageFlipInstance = null;
    let pdfDocInstance = null;
    let currentPageIndex = 0;
    let zoomedPageNumber = 1;

    // Zoom State
    let currentZoomRatio = 1.35;
    let isMouseDown = false;
    let startX = 0, startY = 0, scrollLeft = 0, scrollTop = 0;
    
    // Memory Performance HD Zoom Cache
    const zoomCanvasCache = new Map();

    // --- Render Queue State (chuẩn PDF.js viewer: chỉ render trang cần thiết + pre-render trang kế) ---
    const MAX_CANVAS_PIXELS = 4096 * 4096;   // trần canvas chính thức của PDF.js viewer
    const PAGE_BUFFER_SIZE = 8;              // số trang tối đa giữ canvas đã render (LRU)
    const MAX_CONCURRENT_RENDERS = 2;        // hạn chế render song song
    const pageDivs = [];
    const pageCanvases = [];
    const renderTasks = [];
    const renderedFlags = [];
    const renderingFlags = [];
    let activeRenderCount = 0;
    const renderQueue = [];
    let zoomRenderToken = 0;
    let zoomRenderTask = null;
    let keydownBound = false;

    try {
        const loadingTask = pdfjsLib.getDocument(pdfUrl);
        pdfDocInstance = await loadingTask.promise;
        const numPages = pdfDocInstance.numPages;

        container.innerHTML = '';

        // Determine base dimensions based on first page aspect ratio
        const firstPage = await pdfDocInstance.getPage(1);
        const origViewport = firstPage.getViewport({ scale: 1.0 });
        const pdfAspectRatio = origViewport.height / origViewport.width; // e.g. ~1.414 for A4

        const isMobile = window.innerWidth < 992;
        
        let pageWidth, pageHeight;

        if (isMobile) {
            // Full màn hình: Dành khoảng trống chính xác cho Header (48px) + Footer + padding-bottom (~58px)
            const safeBottom = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--safe-area-inset-bottom') || '0', 10) || 0;
            const reservedVertical = 48 + 48 + safeBottom + 6;
            const availableMobileHeight = Math.max(260, window.innerHeight - reservedVertical);
            const availableMobileWidth = window.innerWidth; // 100% full chiều rộng không chừa viền

            let targetWidth = availableMobileWidth;
            let targetHeight = Math.round(targetWidth * pdfAspectRatio);

            // Đảm bảo không bao giờ tràn cả chiều cao lẫn chiều rộng
            if (targetHeight > availableMobileHeight) {
                targetHeight = availableMobileHeight;
                targetWidth = Math.round(targetHeight / pdfAspectRatio);
            }

            pageWidth = targetWidth;
            pageHeight = targetHeight;
        } else {
            // Desktop: 100% full chiều cao màn hình từ mép trên xuống mép dưới
            pageHeight = window.innerHeight;
            pageWidth = Math.round(pageHeight / pdfAspectRatio);

            const availableWidth = window.innerWidth;
            if (pageWidth * 2 > availableWidth) {
                pageWidth = Math.floor(availableWidth / 2);
                pageHeight = Math.round(pageWidth * pdfAspectRatio);
            }
        }

        // Tạo pageDiv cho toàn bộ trang nhưng KHÔNG render đồng loạt (StPageFlip cần đủ phần tử DOM)
        for (let i = 1; i <= numPages; i++) {
            const pageDiv = document.createElement('div');
            pageDiv.className = 'stpageflip-page';
            pageDiv.setAttribute('data-density', 'soft');
            pageDiv.setAttribute('data-page-num', i);
            pageDiv.style.width = pageWidth + 'px';
            pageDiv.style.height = pageHeight + 'px';

            const canvas = document.createElement('canvas');
            pageDiv.appendChild(canvas);
            container.appendChild(pageDiv);

            pageDivs.push(pageDiv);
            pageCanvases.push(canvas);
            renderTasks.push(null);
            renderedFlags.push(false);
            renderingFlags.push(false);
        }

        // FIX bug trang cuối: với số trang LẺ, createSpread() của StPageFlip biến trang cuối thành
        // spread đơn + density "hard" (pivot tại cạnh gáy + backface-visibility:hidden) → hiệu ứng
        // lật tới trang cuối bị "văng". Thêm 1 trang trống để tổng số trang CHẴN → spread cuối
        // là cặp soft bình thường (xác nhận bởi phân tích source page-flip v2.0.7).
        if (numPages % 2 === 1) {
            const blankPage = document.createElement('div');
            blankPage.className = 'stpageflip-page';
            blankPage.setAttribute('data-density', 'soft');
            blankPage.setAttribute('data-page-num', 'blank');
            blankPage.style.width = pageWidth + 'px';
            blankPage.style.height = pageHeight + 'px';
            container.appendChild(blankPage);
            pageDivs.push(blankPage);
        }

        // --- Render Queue: 1 render task/page, giới hạn 2 task song song, hủy task xa khi lật trang ---
        const renderScale = Math.min(window.devicePixelRatio || 1.5, 1.8);

        // Clamp scale theo maxCanvasPixels (khuyến nghị chính thức PDF.js: 4096x4096)
        const clampScaleForPage = (page, desiredScale) => {
            const vp = page.getViewport({ scale: 1.0 });
            const maxScale = Math.sqrt(MAX_CANVAS_PIXELS / (vp.width * vp.height));
            return Math.min(desiredScale, Math.max(1, maxScale));
        };

        const renderPage = async (pageNum) => {
            if (pageNum < 1 || pageNum > numPages) return;
            const idx = pageNum - 1;
            if (renderedFlags[idx] || renderingFlags[idx]) return;
            if (activeRenderCount >= MAX_CONCURRENT_RENDERS) { renderQueue.push(pageNum); return; }

            renderingFlags[idx] = true;
            activeRenderCount++;
            try {
                const page = await pdfDocInstance.getPage(pageNum);
                const canvas = pageCanvases[idx];
                const scale = clampScaleForPage(page, renderScale);
                const viewport = page.getViewport({ scale });
                canvas.width = viewport.width;
                canvas.height = viewport.height;
                canvas.style.width = '100%';
                canvas.style.height = '100%';
                const context = canvas.getContext('2d');
                const renderTask = page.render({ canvasContext: context, viewport });
                renderTasks[idx] = renderTask;
                try {
                    await renderTask.promise;
                    renderedFlags[idx] = true;
                    evictFarPages(idx);
                } catch (err) {
                    if (err.name !== 'RenderingCancelledException') {
                        console.error('Render error page', pageNum, err);
                    }
                }
            } catch (err) {
                console.error('getPage error', pageNum, err);
            } finally {
                renderingFlags[idx] = false;
                renderTasks[idx] = null;
                activeRenderCount--;
                const next = renderQueue.shift();
                if (next && !renderedFlags[next - 1] && !renderingFlags[next - 1]) renderPage(next);
            }
        };

        // Pre-render: spread trước + spread hiện tại + spread kế.
        // QUAN TRỌNG: source StPageFlip xác nhận flip event chỉ bắn SAU animation (onAnimateEnd →
        // turnToNextPage → updatePageIndex), nên phải render sẵn spread kế để lật xong không bị trang trắng.
        const ensureVisibleRendered = (index) => {
            // Hủy render task cách xa hơn 4 trang so với spread hiện tại
            for (let i = 0; i < numPages; i++) {
                const task = renderTasks[i];
                if (task && Math.abs(i - index) > 4) task.cancel();
            }
            // Dọn queue khỏi các trang đã quá xa (tránh render lãng phí khi lật nhanh)
            for (let i = renderQueue.length - 1; i >= 0; i--) {
                if (Math.abs(renderQueue[i] - 1 - index) > 4) renderQueue.splice(i, 1);
            }
            // 1-based targets: previous spread + current spread + next spread
            const targets = [index - 1, index, index + 1, index + 2, index + 3, index + 4];
            for (const t of targets) renderPage(t);
        };

        // LRU buffer: giữ tối đa PAGE_BUFFER_SIZE trang đã render; zeroing canvas khi evict (giải phóng GPU ngay, chuẩn PDF.js viewer)
        const evictFarPages = (currentIndex) => {
            const rendered = [];
            for (let i = 0; i < numPages; i++) {
                if (renderedFlags[i] && !renderingFlags[i]) rendered.push(i);
            }
            if (rendered.length <= PAGE_BUFFER_SIZE) return;
            rendered.sort((a, b) => Math.abs(a - currentIndex) - Math.abs(b - currentIndex));
            for (let i = PAGE_BUFFER_SIZE; i < rendered.length; i++) {
                const idx = rendered[i];
                if (renderTasks[idx]) { renderTasks[idx].cancel(); renderTasks[idx] = null; }
                const canvas = pageCanvases[idx];
                canvas.width = 0;
                canvas.height = 0;
                renderedFlags[idx] = false;
            }
        };

        // Initialize StPageFlip theo source chính thức (Nodlik/StPageFlip v2.0.7):
        // - autoSize:true BẮT BUỘC với size:"stretch" (source: autoSize set container width=100%;
        //   nếu false, container co về minWidth → sách bị thu nhỏ ~260px/trang)
        // - usePortrait:isMobile (source: chế độ portrait dùng 1 trang/lật, giữ nguyên UX mobile gốc)
        // - maxShadowOpacity:0 + drawShadow:false + showPageCorners:false (giảm GPU mỗi frame lật)
        // maxWidth động theo chiều cao viewport: stretch mode tính pageWidth = min(containerWidth/2, maxWidth)
        // và pageHeight = pageWidth×aspect. Với maxWidth = innerHeight×0.94/aspect thì trang luôn ≤ 94%
        // chiều cao viewport → sách không bao giờ bị cắt (tràn ngoài overflow:hidden) và lớn nhất có thể.
        // (Trước đây maxWidth cố định 900 → trên 1080p sách 900×1272 cao hơn viewport nên bị cắt, trông nhỏ/vỡ.)
        const maxPageW = isMobile ? pageWidth : Math.floor((window.innerHeight * 0.94) / pdfAspectRatio);
        const maxPageH = isMobile ? pageHeight : Math.floor(window.innerHeight * 0.94);
        pageFlipInstance = new St.PageFlip(container, {
            width: pageWidth,
            height: pageHeight,
            size: isMobile ? "fixed" : "stretch",
            minWidth: isMobile ? 200 : 260,
            maxWidth: maxPageW,
            minHeight: isMobile ? 280 : 360,
            maxHeight: maxPageH,
            autoSize: true,
            maxShadowOpacity: 0,
            drawShadow: false,
            showCover: false,
            mobileScrollSupport: true,
            usePortrait: isMobile,
            showPageCorners: false,
            flippingTime: 600,
            startPage: 0
        });

        // Đăng ký sự kiện init TRƯỚC loadFromHTML (README chính thức: listen 'init' before loadFrom...)
        pageFlipInstance.on('init', () => {
            if (skeleton) skeleton.style.display = 'none';
            container.style.display = 'block';
            // FIX kích thước: lần đo đầu của thư viện có thể xảy ra khi layout chưa ổn định
            // (skeleton chiếm flex space → container bị nén xuống min-height 360px → trang bị
            // clamp 270×360 và cache vĩnh viễn). update() = render.update() + pages.show()
            // sẽ tính lại boundsRect với layout cuối và vẽ lại trang theo đúng kích thước.
            pageFlipInstance.update();
        });

        pageFlipInstance.loadFromHTML(pageDivs);

        // Fallback an toàn: ẩn skeleton nếu init event không kích hoạt (phòng thư viện không gọi)
        setTimeout(() => {
            if (skeleton) skeleton.style.display = 'none';
            container.style.display = 'block';
        }, 2500);

        const formatPageNumber = (n) => String(n).padStart(2, '0');

        const updateIndicator = (index) => {
            currentPageIndex = index;
            const current = Math.min(index + 1, numPages);
            const text = `${formatPageNumber(current)} / ${formatPageNumber(numPages)}`;
            if (pageIndicator) pageIndicator.innerText = text;
            if (pageIndicatorMobile) pageIndicatorMobile.innerText = text;
        };

        // Render lazy theo trang hiển thị: chỉ render 2 trang đầu ngay khi mở sách
        ensureVisibleRendered(0);

        pageFlipInstance.on('flip', (e) => {
            updateIndicator(e.data);
            ensureVisibleRendered(e.data);
        });

        // Bắt lật SỚM: khi animation bắt đầu (state "flipping"), render ngay spread mục tiêu
        // trong 600ms animation để lật xong trang đã sẵn sàng (không chờ flip event cuối animation)
        pageFlipInstance.on('changeState', (e) => {
            if (e.data === 'flipping') ensureVisibleRendered(currentPageIndex);
        });

        updateIndicator(0);

        if (btnPrev) btnPrev.addEventListener('click', () => pageFlipInstance.flipPrev());
        if (btnNext) btnNext.addEventListener('click', () => pageFlipInstance.flipNext());
        if (btnPrevMobile) btnPrevMobile.addEventListener('click', () => pageFlipInstance.flipPrev());
        if (btnNextMobile) btnNextMobile.addEventListener('click', () => pageFlipInstance.flipNext());

        // --- High Performance Smart Zoom Single Page HD Viewer Engine ---
        function applyZoomTransform() {
            zoomCanvas.style.transform = `scale(${currentZoomRatio})`;
            zoomLevelText.innerText = `${Math.round(currentZoomRatio * 100)}%`;
        }

        async function renderZoomCanvas(pageNum) {
            if (!pdfDocInstance || pageNum < 1 || pageNum > numPages) return;
            zoomedPageNumber = pageNum;

            zoomPageTitle.innerText = `Trang ${formatPageNumber(pageNum)} / ${formatPageNumber(numPages)} (Bản Siêu Nét HD)`;

            // Check On-Demand HD Memory Cache
            if (zoomCanvasCache.has(pageNum)) {
                const cached = zoomCanvasCache.get(pageNum);
                zoomCanvas.width = cached.width;
                zoomCanvas.height = cached.height;
                zoomCanvas.style.width = cached.styleWidth;
                zoomCanvas.style.height = cached.styleHeight;
                zoomCanvas.getContext('2d').drawImage(cached.canvas, 0, 0);
                return;
            }

            const token = ++zoomRenderToken;

            // API PDF.js cấm render 2 trang lên cùng canvas cùng lúc: hủy render zoom cũ trước khi render mới
            if (zoomRenderTask) {
                try { zoomRenderTask.cancel(); } catch (e) { /* ignore */ }
                zoomRenderTask = null;
            }

            const page = await pdfDocInstance.getPage(pageNum);
            if (token !== zoomRenderToken) return; // đã có yêu cầu mới hơn → bỏ kết quả cũ

            // Render lên offscreen duy nhất (không nhân bản), scale clamp theo maxCanvasPixels
            const baseViewport = page.getViewport({ scale: 1.0 });
            const maxScale = Math.sqrt(MAX_CANVAS_PIXELS / (baseViewport.width * baseViewport.height));
            const scale = Math.min(2.0, Math.max(1, maxScale));
            const viewport = page.getViewport({ scale });

            const fitWidth = Math.min(window.innerWidth * 0.85, 960);
            const fitHeight = Math.round(fitWidth * (viewport.height / viewport.width));

            const offscreenCanvas = document.createElement('canvas');
            offscreenCanvas.width = viewport.width;
            offscreenCanvas.height = viewport.height;
            const offCtx = offscreenCanvas.getContext('2d');
            const task = page.render({ canvasContext: offCtx, viewport });
            zoomRenderTask = task;
            try {
                await task.promise;
            } catch (err) {
                if (err.name !== 'RenderingCancelledException') console.error(err);
                return;
            } finally {
                zoomRenderTask = null;
            }
            if (token !== zoomRenderToken) return; // đã có yêu cầu mới hơn → bỏ kết quả cũ

            zoomCanvas.width = viewport.width;
            zoomCanvas.height = viewport.height;
            zoomCanvas.style.width = fitWidth + 'px';
            zoomCanvas.style.height = fitHeight + 'px';
            zoomCanvas.getContext('2d').drawImage(offscreenCanvas, 0, 0);

            // LRU Cache eviction: giới hạn 3 trang (giảm từ 5) để tiết kiệm bộ nhớ
            if (zoomCanvasCache.size >= 3) {
                const oldestKey = zoomCanvasCache.keys().next().value;
                zoomCanvasCache.delete(oldestKey);
            }
            zoomCanvasCache.set(pageNum, {
                canvas: offscreenCanvas,
                width: viewport.width,
                height: viewport.height,
                styleWidth: fitWidth + 'px',
                styleHeight: fitHeight + 'px'
            });
        }

        async function openSmartZoomSingleModal(targetPageNum) {
            const target = Math.min(targetPageNum || (currentPageIndex + 1), numPages);
            await renderZoomCanvas(target);

            currentZoomRatio = 1.35; // Default 135% zoom ratio
            applyZoomTransform();

            zoomOverlay.classList.add('show');
            zoomStage.scrollTop = 0;
            zoomStage.scrollLeft = 0;
        }

        function closeSmartZoomModal() {
            zoomOverlay.classList.remove('show');
        }

        if (btnZoomPage) btnZoomPage.addEventListener('click', () => openSmartZoomSingleModal(currentPageIndex + 1));
        if (btnZoomClose) btnZoomClose.addEventListener('click', closeSmartZoomModal);

        // Next / Prev Page controls directly inside Zoom Overlay!
        if (btnZoomPrev) {
            btnZoomPrev.addEventListener('click', async () => {
                if (zoomedPageNumber > 1) {
                    await renderZoomCanvas(zoomedPageNumber - 1);
                }
            });
        }
        if (btnZoomNext) {
            btnZoomNext.addEventListener('click', async () => {
                if (zoomedPageNumber < numPages) {
                    await renderZoomCanvas(zoomedPageNumber + 1);
                }
            });
        }

        // Zoom Controls (+ / - / Reset)
        if (btnZoomIn) {
            btnZoomIn.addEventListener('click', () => {
                currentZoomRatio = Math.min(3.0, currentZoomRatio + 0.25);
                applyZoomTransform();
            });
        }
        if (btnZoomOut) {
            btnZoomOut.addEventListener('click', () => {
                currentZoomRatio = Math.max(0.8, currentZoomRatio - 0.25);
                applyZoomTransform();
            });
        }
        if (btnZoomReset) {
            btnZoomReset.addEventListener('click', () => {
                currentZoomRatio = 1.0;
                applyZoomTransform();
            });
        }

        // Click & Drag Native Scroll Panning
        zoomStage.addEventListener('mousedown', (e) => {
            isMouseDown = true;
            startX = e.pageX - zoomStage.offsetLeft;
            startY = e.pageY - zoomStage.offsetTop;
            scrollLeft = zoomStage.scrollLeft;
            scrollTop = zoomStage.scrollTop;
        });

        zoomStage.addEventListener('mouseleave', () => { isMouseDown = false; });
        zoomStage.addEventListener('mouseup', () => { isMouseDown = false; });

        zoomStage.addEventListener('mousemove', (e) => {
            if (!isMouseDown) return;
            e.preventDefault();
            const x = e.pageX - zoomStage.offsetLeft;
            const y = e.pageY - zoomStage.offsetTop;
            const walkX = (x - startX) * 1.5;
            const walkY = (y - startY) * 1.5;
            zoomStage.scrollLeft = scrollLeft - walkX;
            zoomStage.scrollTop = scrollTop - walkY;
        });


        // Keyboard navigation inside Zoom Overlay (guard chống double-bind)
        if (!keydownBound) {
        keydownBound = true;
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeSmartZoomModal();
            } else if (e.key === 'ArrowLeft') {
                if (zoomOverlay.classList.contains('show')) {
                    if (zoomedPageNumber > 1) renderZoomCanvas(zoomedPageNumber - 1);
                } else {
                    pageFlipInstance.flipPrev();
                }
            } else if (e.key === 'ArrowRight') {
                if (zoomOverlay.classList.contains('show')) {
                    if (zoomedPageNumber < numPages) renderZoomCanvas(zoomedPageNumber + 1);
                } else {
                    pageFlipInstance.flipNext();
                }
            }
        });
        }

        // Cleanup instance on page unload according to official API docs
        window.addEventListener('beforeunload', () => {
            for (let i = 0; i < numPages; i++) {
                if (renderTasks[i]) { renderTasks[i].cancel(); renderTasks[i] = null; }
            }
            if (pageFlipInstance) {
                pageFlipInstance.destroy();
            }
            if (pdfDocInstance) {
                try { pdfDocInstance.destroy(); } catch (e) { /* ignore */ }
            }
            zoomCanvasCache.clear();
        });

    } catch (err) {
        console.error("Flipbook render error:", err);
        if (skeleton) skeleton.style.display = 'none';
        const errP = document.createElement('p');
        errP.style.cssText = 'color: #e74c3c; font-size: 0.85rem; padding: 2rem;';
        const errIcon = document.createElement('i');
        errIcon.className = 'ti ti-alert-triangle';
        errP.appendChild(errIcon);
        errP.appendChild(document.createTextNode(' Không thể tải file PDF (' + (err.message || 'Lỗi không xác định') + ')'));
        wrapper.innerHTML = '';
        wrapper.appendChild(errP);
    }
});
