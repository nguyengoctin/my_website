// Command Palette Search Modal Module (with Vietnamese diacritics support & 2-column rich preview)
(function () {
    'use strict';

    let searchModal = null;
    let searchInput = null;
    let resultsList = null;
    let resultsColumn = null;
    let previewContent = null;
    let previewPlaceholder = null;
    let stateInitial = null;
    let stateEmpty = null;
    let searchLoading = null;
    let searchClearBtn = null;
    let resultsCountEl = null;

    let searchIndexData = [];
    let isDataLoaded = false;
    let isLoading = false;
    let searchResults = [];
    let activeIndex = -1;
    let debounceTimer = null;
    let isComposing = false; // Xử lý bộ gõ Telex / VNI

    // Hàm chuẩn hóa tiếng Việt: bỏ dấu, lowercase để tìm kiếm mờ mượt mà
    function normalizeVietnamese(str) {
        if (!str) return '';
        return str
            .toString()
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/[đĐ]/g, 'd')
            .replace(/[^a-z0-9\s]/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
    }

    // Tải dữ liệu index từ file JSON sinh bởi Hugo
    async function loadIndexData() {
        if (isDataLoaded || isLoading) return;
        isLoading = true;
        if (searchLoading) searchLoading.style.display = 'inline';

        try {
            const indexUrl = window.searchConfig?.lunrIndexURL || '/index.json';
            const response = await fetch(indexUrl);
            if (!response.ok) throw new Error('Failed to load search index');
            const data = await response.json();
            
            // Xử lý chuẩn hóa từ trước để tìm kiếm siêu tốc
            searchIndexData = data.map((item, idx) => {
                const titleNorm = normalizeVietnamese(item.title || '');
                const contentNorm = normalizeVietnamese(item.content || '');
                const tagsNorm = Array.isArray(item.tags) ? item.tags.map(t => normalizeVietnamese(t)).join(' ') : '';
                const categoriesNorm = Array.isArray(item.categories) ? item.categories.map(c => normalizeVietnamese(c)).join(' ') : '';

                return {
                    id: idx,
                    uri: item.uri || item.permalink || '#',
                    title: item.title || 'Không có tiêu đề',
                    date: item.date || '',
                    tags: Array.isArray(item.tags) ? item.tags : (item.tags ? [item.tags] : []),
                    categories: Array.isArray(item.categories) ? item.categories : (item.categories ? [item.categories] : []),
                    content: item.content || '',
                    titleNorm: titleNorm,
                    contentNorm: contentNorm,
                    tagsNorm: tagsNorm,
                    categoriesNorm: categoriesNorm,
                    combinedNorm: `${titleNorm} ${tagsNorm} ${categoriesNorm} ${contentNorm}`
                };
            });
            isDataLoaded = true;
        } catch (error) {
            console.error('Search index load error:', error);
        } finally {
            isLoading = false;
            if (searchLoading) searchLoading.style.display = 'none';
        }
    }

    // Thực hiện tìm kiếm
    function performSearch(query) {
        const rawQuery = query.trim();
        const normQuery = normalizeVietnamese(rawQuery);

        if (!normQuery) {
            searchResults = [];
            activeIndex = -1;
            renderResults();
            return;
        }

        const queryTokens = normQuery.split(' ').filter(t => t.length > 0);

        // Tính điểm scoring cho từng bài
        const scored = [];

        for (let i = 0; i < searchIndexData.length; i++) {
            const item = searchIndexData[i];
            let score = 0;
            let matchedAll = true;

            // Kiểm tra xem tất cả token có nằm trong bài viết không
            for (let t = 0; t < queryTokens.length; t++) {
                const token = queryTokens[t];
                let tokenMatched = false;

                if (item.titleNorm.includes(token)) {
                    score += 100;
                    if (item.titleNorm.startsWith(token)) score += 50;
                    tokenMatched = true;
                }
                if (item.tagsNorm.includes(token)) {
                    score += 40;
                    tokenMatched = true;
                }
                if (item.categoriesNorm.includes(token)) {
                    score += 30;
                    tokenMatched = true;
                }
                if (item.contentNorm.includes(token)) {
                    score += 10;
                    tokenMatched = true;
                }

                if (!tokenMatched) {
                    matchedAll = false;
                    break;
                }
            }

            if (matchedAll && score > 0) {
                // Trích xuất đoạn snippet xung quanh từ khóa
                const snippet = extractSnippet(item.content, queryTokens, 180);
                scored.push({
                    item: item,
                    score: score,
                    snippet: snippet
                });
            }
        }

        // Sắp xếp theo điểm giảm dần
        scored.sort((a, b) => b.score - a.score);
        searchResults = scored.slice(0, 20); // Giới hạn 20 kết quả hàng đầu
        activeIndex = searchResults.length > 0 ? 0 : -1;
        renderResults(rawQuery);
    }

    // Trích xuất đoạn ngữ cảnh snippet
    function extractSnippet(content, tokens, length) {
        if (!content) return '';
        const normContent = normalizeVietnamese(content);
        let firstPos = -1;

        for (let i = 0; i < tokens.length; i++) {
            const pos = normContent.indexOf(tokens[i]);
            if (pos !== -1 && (firstPos === -1 || pos < firstPos)) {
                firstPos = pos;
            }
        }

        if (firstPos === -1) {
            return content.slice(0, length) + (content.length > length ? '...' : '');
        }

        let start = Math.max(0, firstPos - 40);
        let end = Math.min(content.length, firstPos + length);

        if (start > 0) {
            const spaceIdx = content.indexOf(' ', start);
            if (spaceIdx !== -1 && spaceIdx < firstPos) start = spaceIdx + 1;
        }

        let snippet = content.substring(start, end);
        if (start > 0) snippet = '...' + snippet;
        if (end < content.length) snippet = snippet + '...';

        return snippet;
    }

    // Highlight từ khóa
    function highlightKeywords(text, queryTokens) {
        if (!text || !queryTokens || queryTokens.length === 0) return text;
        let escapedTokens = queryTokens.map(t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
        if (!escapedTokens) return text;
        const regex = new RegExp(`(${escapedTokens})`, 'gi');
        return text.replace(regex, '<mark class="search-highlight">$1</mark>');
    }

    // Render danh sách kết quả và update preview
    function renderResults(rawQuery = '') {
        const queryTokens = normalizeVietnamese(rawQuery).split(' ').filter(t => t.length > 0);

        if (!rawQuery.trim()) {
            if (stateInitial) stateInitial.style.display = 'flex';
            if (stateEmpty) stateEmpty.style.display = 'none';
            if (resultsList) resultsList.innerHTML = '';
            if (resultsCountEl) resultsCountEl.textContent = '0 kết quả';
            renderPreview(null);
            return;
        }

        if (stateInitial) stateInitial.style.display = 'none';

        if (searchResults.length === 0) {
            if (stateEmpty) stateEmpty.style.display = 'flex';
            if (resultsList) resultsList.innerHTML = '';
            if (resultsCountEl) resultsCountEl.textContent = '0 kết quả';
            renderPreview(null);
            return;
        }

        if (stateEmpty) stateEmpty.style.display = 'none';
        if (resultsCountEl) resultsCountEl.textContent = `${searchResults.length} kết quả`;

        let html = '';
        searchResults.forEach((res, idx) => {
            const item = res.item;
            const isSelected = idx === activeIndex;
            const titleHighlighted = highlightKeywords(item.title, queryTokens);
            const categoryText = item.categories.length > 0 ? item.categories[0] : '';

            html += `
                <li class="search-result-item ${isSelected ? 'selected' : ''}" 
                    data-index="${idx}" 
                    role="option" 
                    aria-selected="${isSelected}">
                    <div class="result-item-main">
                        <div class="result-item-header">
                            <span class="result-title">${titleHighlighted}</span>
                            ${categoryText ? `<span class="result-cat-badge">${categoryText}</span>` : ''}
                        </div>
                        <div class="result-item-meta">
                            ${item.date ? `<span class="result-date"><i class="ti ti-calendar"></i> ${item.date}</span>` : ''}
                            ${item.tags.length > 0 ? `<span class="result-tags"><i class="ti ti-tags"></i> ${item.tags.slice(0, 3).join(', ')}</span>` : ''}
                        </div>
                    </div>
                    <div class="result-item-arrow"><i class="ti ti-chevron-right"></i></div>
                </li>
            `;
        });

        if (resultsList) {
            resultsList.innerHTML = html;
        }

        renderPreview(searchResults[activeIndex] || null, queryTokens);
    }

    // Render cột Live Preview bên phải
    function renderPreview(selectedResult, queryTokens = []) {
        if (!previewContent || !previewPlaceholder) return;

        if (!selectedResult) {
            previewContent.style.display = 'none';
            previewPlaceholder.style.display = 'flex';
            return;
        }

        const item = selectedResult.item;
        const snippet = selectedResult.snippet;

        previewPlaceholder.style.display = 'none';
        previewContent.style.display = 'flex';

        const titleEl = document.getElementById('preview-title');
        const dateEl = document.getElementById('preview-date');
        const catEl = document.getElementById('preview-category');
        const tagsEl = document.getElementById('preview-tags');
        const snippetEl = document.getElementById('preview-snippet');
        const linkEl = document.getElementById('preview-open-link');

        if (titleEl) titleEl.innerHTML = highlightKeywords(item.title, queryTokens);
        
        if (dateEl) {
            if (item.date) {
                dateEl.style.display = 'inline-flex';
                dateEl.querySelector('span').textContent = item.date;
            } else {
                dateEl.style.display = 'none';
            }
        }

        if (catEl) {
            if (item.categories && item.categories.length > 0) {
                catEl.style.display = 'inline-flex';
                catEl.querySelector('span').textContent = item.categories.join(', ');
            } else {
                catEl.style.display = 'none';
            }
        }

        if (tagsEl) {
            if (item.tags && item.tags.length > 0) {
                tagsEl.innerHTML = item.tags.map(t => `<span class="preview-tag-badge">#${t}</span>`).join('');
                tagsEl.style.display = 'flex';
            } else {
                tagsEl.style.display = 'none';
            }
        }

        if (snippetEl) {
            snippetEl.innerHTML = highlightKeywords(snippet, queryTokens);
        }

        if (linkEl) {
            linkEl.href = item.uri;
        }
    }

    // Mở Modal
    function openModal() {
        if (!searchModal) return;
        loadIndexData();
        searchModal.classList.add('active');
        searchModal.setAttribute('aria-hidden', 'false');
        document.body.classList.add('search-modal-open');

        // Tự động đóng mobile menu nếu đang mở
        const menuMobile = document.getElementById('menu-mobile');
        const menuToggleMobile = document.getElementById('menu-toggle-mobile');
        if (menuMobile) menuMobile.classList.remove('active');
        if (menuToggleMobile) menuToggleMobile.classList.remove('active');
        document.body.classList.remove('mobile-menu-open');
        document.body.classList.remove('blur');

        setTimeout(() => {
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }, 50);
    }

    // Đóng Modal
    function closeModal() {
        if (!searchModal) return;
        searchModal.classList.remove('active');
        searchModal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('search-modal-open');
        document.body.classList.remove('blur');
        const headerDesktop = document.getElementById('header-desktop');
        if (headerDesktop) headerDesktop.classList.remove('open');
    }

    // Chọn bài viết đang active
    function navigateToActive() {
        if (activeIndex >= 0 && activeIndex < searchResults.length) {
            const uri = searchResults[activeIndex].item.uri;
            if (uri && uri !== '#') {
                window.location.href = uri;
            }
        }
    }

    // Cập nhật selected state trong danh sách và scroll vào view
    function updateSelectedUI() {
        if (!resultsList) return;
        const items = resultsList.querySelectorAll('.search-result-item');
        items.forEach((item, idx) => {
            if (idx === activeIndex) {
                item.classList.add('selected');
                item.setAttribute('aria-selected', 'true');
                item.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
            } else {
                item.classList.remove('selected');
                item.setAttribute('aria-selected', 'false');
            }
        });

        const rawQuery = searchInput ? searchInput.value : '';
        const queryTokens = normalizeVietnamese(rawQuery).split(' ').filter(t => t.length > 0);
        renderPreview(searchResults[activeIndex] || null, queryTokens);
    }

    // Khởi tạo sự kiện
    function initSearchModal() {
        searchModal = document.getElementById('search-modal');
        if (!searchModal) return;

        searchInput = document.getElementById('modal-search-input');
        resultsList = document.getElementById('search-results-list');
        resultsColumn = document.getElementById('search-results-column');
        previewContent = document.getElementById('preview-content');
        previewPlaceholder = document.getElementById('preview-placeholder');
        stateInitial = document.getElementById('search-state-initial');
        stateEmpty = document.getElementById('search-state-empty');
        searchLoading = document.getElementById('search-loading');
        searchClearBtn = document.getElementById('search-clear-btn');
        resultsCountEl = document.getElementById('footer-results-count');

        const backdrop = document.getElementById('search-modal-backdrop');
        const closeBtn = document.getElementById('search-close-btn');

        // Đóng khi click backdrop hoặc nút ESC
        if (backdrop) backdrop.addEventListener('click', closeModal);
        if (closeBtn) closeBtn.addEventListener('click', closeModal);

        // Nút xóa input
        if (searchClearBtn && searchInput) {
            searchClearBtn.addEventListener('click', () => {
                searchInput.value = '';
                searchClearBtn.style.display = 'none';
                performSearch('');
                searchInput.focus();
            });
        }

        // Lắng nghe gõ phím trên input
        if (searchInput) {
            searchInput.addEventListener('compositionstart', () => {
                isComposing = true;
            });
            searchInput.addEventListener('compositionend', () => {
                isComposing = false;
                performSearch(searchInput.value);
            });

            searchInput.addEventListener('input', () => {
                if (searchClearBtn) {
                    searchClearBtn.style.display = searchInput.value ? 'inline-flex' : 'none';
                }
                if (isComposing) return;
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(() => {
                    performSearch(searchInput.value);
                }, 150);
            });

            searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    if (searchResults.length > 0) {
                        activeIndex = (activeIndex + 1) % searchResults.length;
                        updateSelectedUI();
                    }
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    if (searchResults.length > 0) {
                        activeIndex = (activeIndex - 1 + searchResults.length) % searchResults.length;
                        updateSelectedUI();
                    }
                } else if (e.key === 'Enter') {
                    e.preventDefault();
                    navigateToActive();
                } else if (e.key === 'Escape') {
                    e.preventDefault();
                    closeModal();
                }
            });
        }

        // Click trên item kết quả
        if (resultsList) {
            resultsList.addEventListener('click', (e) => {
                const itemEl = e.target.closest('.search-result-item');
                if (itemEl) {
                    const idx = parseInt(itemEl.getAttribute('data-index'), 10);
                    if (!isNaN(idx)) {
                        activeIndex = idx;
                        updateSelectedUI();
                        navigateToActive();
                    }
                }
            });

            resultsList.addEventListener('mousemove', (e) => {
                const itemEl = e.target.closest('.search-result-item');
                if (itemEl) {
                    const idx = parseInt(itemEl.getAttribute('data-index'), 10);
                    if (!isNaN(idx) && idx !== activeIndex) {
                        activeIndex = idx;
                        updateSelectedUI();
                    }
                }
            });
        }

        // Lắng nghe Shortcut toàn trang: Ctrl+K, Cmd+K, /
        document.addEventListener('keydown', (e) => {
            const activeTag = document.activeElement ? document.activeElement.tagName.toLowerCase() : '';
            const isEditable = document.activeElement && (document.activeElement.isContentEditable || activeTag === 'input' || activeTag === 'textarea' || activeTag === 'select');

            if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
                e.preventDefault();
                if (searchModal.classList.contains('active')) {
                    closeModal();
                } else {
                    openModal();
                }
            } else if (e.key === '/' && !isEditable) {
                e.preventDefault();
                openModal();
            } else if (e.key === 'Escape' && searchModal.classList.contains('active')) {
                e.preventDefault();
                closeModal();
            }
        });

        // Gắn sự kiện cho các nút trigger tìm kiếm trên Header
        document.querySelectorAll('.search-button, [data-search-trigger="modal"], #search-toggle-desktop, #search-toggle-mobile').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                document.body.classList.remove('blur');
                openModal();
            }, true);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSearchModal);
    } else {
        initSearchModal();
    }
})();
