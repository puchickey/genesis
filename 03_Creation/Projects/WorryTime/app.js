// ===== Worry Time MVP v3 =====
// Topic-based sessions with date dividers

(function () {
    'use strict';

    const STORAGE_KEY = 'worryTime';
    const DEFAULT_STATE = {
        config: { startHour: 21, startMinute: 0, durationMinutes: 20 },
        sessions: [],
        activeSessionId: null
    };

    // SVG icons
    const ICON = {
        bubble: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
        close: '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>',
        clock: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
    };

    // ----- State -----
    let state = loadState();
    let isWorryTime = false;

    // ----- DOM -----
    const $ = (s) => document.querySelector(s);
    const pageDoor = $('#page-door');
    const pageMemo = $('#page-memo');
    const door = $('#door');
    const doorContainer = $('#door-container');
    const countdownLabel = $('#countdown-label');
    const countdownTime = $('#countdown-time');
    const scheduleLabel = $('#schedule-label');
    const btnSettings = $('#btn-settings');
    const btnBack = $('#btn-back');
    const btnNewTopic = $('#btn-new-topic');
    const sessionList = $('#session-list');
    const memoTitle = $('#memo-title');
    const btnDeleteTopic = $('#btn-delete-topic');
    const memoItems = $('#memo-items');
    const freeWrite = $('#free-write');
    const btnSend = $('#btn-send');
    const settingsDialog = $('#settings-dialog');
    const setHour = $('#set-hour');
    const setMinute = $('#set-minute');
    const setDuration = $('#set-duration');
    const btnSettingsCancel = $('#btn-settings-cancel');
    const btnSettingsSave = $('#btn-settings-save');

    // ----- Persistence -----
    function loadState() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (raw) {
                const parsed = JSON.parse(raw);
                return { ...DEFAULT_STATE, ...parsed };
            }
        } catch (e) { /* ignore */ }
        return JSON.parse(JSON.stringify(DEFAULT_STATE));
    }

    function saveState() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    }

    // ----- Helpers -----
    function genId() {
        return Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
    }

    function getWorryStartToday() {
        const d = new Date();
        d.setHours(state.config.startHour, state.config.startMinute, 0, 0);
        return d;
    }

    function getWorryEndToday() {
        return new Date(getWorryStartToday().getTime() + state.config.durationMinutes * 60000);
    }

    function checkIsWorryTime() {
        const now = new Date();
        return now >= getWorryStartToday() && now < getWorryEndToday();
    }

    function getSecondsUntilStart() {
        const now = new Date();
        let start = getWorryStartToday();
        if (now >= getWorryEndToday()) start.setDate(start.getDate() + 1);
        return Math.max(0, Math.floor((start - now) / 1000));
    }

    function getSecondsRemaining() {
        return Math.max(0, Math.floor((getWorryEndToday() - new Date()) / 1000));
    }

    function fmt(sec) {
        const h = Math.floor(sec / 3600);
        const m = Math.floor((sec % 3600) / 60);
        const s = sec % 60;
        return h > 0
            ? `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
            : `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }

    function dateLabel(ts) {
        const d = new Date(ts);
        return `${d.getMonth() + 1}/${d.getDate()}`;
    }

    function timeLabel(ts) {
        const d = new Date(ts);
        return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
    }

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // ----- Session helpers -----
    function getActiveSession() {
        return state.sessions.find(s => s.id === state.activeSessionId) || null;
    }

    function createSession(title) {
        const session = {
            id: genId(),
            title: title || 'New Topic',
            createdAt: new Date().toISOString(),
            messages: []
        };
        state.sessions.unshift(session);
        state.activeSessionId = session.id;
        saveState();
        return session;
    }

    function selectSession(id) {
        state.activeSessionId = id;
        saveState();
        renderSidebar();
        renderMain();
    }

    function deleteSession(id) {
        state.sessions = state.sessions.filter(s => s.id !== id);
        if (state.activeSessionId === id) {
            state.activeSessionId = state.sessions.length > 0 ? state.sessions[0].id : null;
        }
        saveState();
        renderSidebar();
        renderMain();
    }

    // ----- Page Navigation -----
    function showPage(page) {
        [pageDoor, pageMemo].forEach(p => {
            p.classList.remove('active', 'exit-left');
        });
        if (page === 'memo') {
            pageDoor.classList.add('exit-left');
            pageMemo.classList.add('active');
        } else {
            pageDoor.classList.add('active');
        }
    }

    // ----- Door -----
    function updateDoor() {
        if (isWorryTime) {
            door.classList.remove('closed');
            door.classList.add('open');
            doorContainer.classList.add('active');
        } else {
            door.classList.remove('open');
            door.classList.add('closed');
            doorContainer.classList.remove('active');
        }
    }

    // ----- Render Sidebar -----
    function renderSidebar() {
        sessionList.innerHTML = '';

        if (state.sessions.length === 0) {
            sessionList.innerHTML = '<div class="memo-empty">—</div>';
            return;
        }

        state.sessions.forEach(session => {
            const btn = document.createElement('button');
            btn.className = 'session-item' + (session.id === state.activeSessionId ? ' active' : '');
            btn.textContent = session.title;
            btn.addEventListener('click', () => selectSession(session.id));
            sessionList.appendChild(btn);
        });
    }

    // ----- Render Main (messages grouped by date) -----
    function renderMain() {
        const session = getActiveSession();

        if (!session) {
            memoTitle.textContent = '';
            memoItems.innerHTML = '<div class="memo-empty">—</div>';
            return;
        }

        memoTitle.textContent = session.title;

        memoItems.innerHTML = '';

        if (session.messages.length === 0) {
            memoItems.innerHTML = '<div class="memo-empty">' + ICON.bubble + '</div>';
            return;
        }

        // Group messages by date
        let currentDate = '';
        session.messages.forEach((msg, idx) => {
            const msgDate = msg.ts.split('T')[0];
            const label = dateLabel(msg.ts);

            // Insert date divider if new date
            if (msgDate !== currentDate) {
                currentDate = msgDate;
                const divider = document.createElement('div');
                divider.className = 'date-divider';
                divider.textContent = label;
                memoItems.appendChild(divider);
            }

            // Message card
            const card = document.createElement('div');
            card.className = 'memo-card';
            card.innerHTML = `
                <span class="memo-icon">${ICON.bubble}</span>
                <span class="memo-text">${escapeHtml(msg.text)}</span>
                <span class="memo-time">${timeLabel(msg.ts)}</span>
                <button class="btn-memo-delete" data-idx="${idx}">${ICON.close}</button>
            `;
            memoItems.appendChild(card);
        });

        // Bind delete
        memoItems.querySelectorAll('.btn-memo-delete').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const target = e.target.closest('.btn-memo-delete');
                const idx = parseInt(target.dataset.idx);
                session.messages.splice(idx, 1);
                saveState();
                renderMain();
            });
        });

        // Scroll to bottom
        memoItems.scrollTop = memoItems.scrollHeight;
    }

    // ----- Send -----
    function sendMemo() {
        const text = freeWrite.value.trim();
        if (!text) return;

        let session = getActiveSession();
        if (!session) {
            // Auto-create a session if none exists
            session = createSession('New Topic');
            renderSidebar();
        }

        session.messages.push({ text, ts: new Date().toISOString() });
        saveState();
        freeWrite.value = '';
        renderMain();
    }

    // ----- Tick -----
    function tick() {
        const was = isWorryTime;
        isWorryTime = checkIsWorryTime();

        if (!was && isWorryTime) updateDoor();
        if (was && !isWorryTime) {
            updateDoor();
            if (pageMemo.classList.contains('active')) showPage('door');
        }

        // Schedule label (always visible)
        const sh = String(state.config.startHour).padStart(2, '0');
        const sm = String(state.config.startMinute).padStart(2, '0');
        const endDate = getWorryEndToday();
        const eh = String(endDate.getHours()).padStart(2, '0');
        const em = String(endDate.getMinutes()).padStart(2, '0');
        scheduleLabel.textContent = `${sh}:${sm} — ${eh}:${em}`;

        if (isWorryTime) {
            countdownLabel.textContent = 'REMAINING';
            countdownTime.textContent = fmt(getSecondsRemaining());
            countdownTime.classList.add('active');
        } else {
            countdownLabel.textContent = 'NEXT';
            countdownTime.textContent = fmt(getSecondsUntilStart());
            countdownTime.classList.remove('active');
        }
    }

    // ===== EVENT LISTENERS =====

    // Door → open page 2
    doorContainer.addEventListener('click', () => {
        if (!isWorryTime) return;
        renderSidebar();
        renderMain();
        showPage('memo');
    });

    // Back button
    btnBack.addEventListener('click', () => showPage('door'));

    // New Topic
    btnNewTopic.addEventListener('click', () => {
        createSession('New Topic');
        renderSidebar();
        renderMain();
        // Focus on title for immediate renaming
        memoTitle.focus();
        // Select all text for easy replacement
        const range = document.createRange();
        range.selectNodeContents(memoTitle);
        const sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    });

    // Title editing (save on blur or Enter)
    memoTitle.addEventListener('blur', () => {
        const session = getActiveSession();
        if (!session) return;
        const newTitle = memoTitle.textContent.trim() || 'Untitled';
        session.title = newTitle;
        saveState();
        renderSidebar();
    });

    memoTitle.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            memoTitle.blur();
        }
    });

    // Delete topic
    btnDeleteTopic.addEventListener('click', () => {
        const session = getActiveSession();
        if (!session) return;
        deleteSession(session.id);
    });

    // Send
    btnSend.addEventListener('click', sendMemo);

    freeWrite.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMemo();
        }
    });

    // Settings
    btnSettings.addEventListener('click', () => {
        setHour.value = state.config.startHour;
        setMinute.value = state.config.startMinute;
        setDuration.value = state.config.durationMinutes;
        settingsDialog.showModal();
    });

    btnSettingsSave.addEventListener('click', () => {
        state.config.startHour = parseInt(setHour.value) || 21;
        state.config.startMinute = parseInt(setMinute.value) || 0;
        state.config.durationMinutes = parseInt(setDuration.value) || 20;
        saveState();
        settingsDialog.close();
        tick();
    });

    btnSettingsCancel.addEventListener('click', () => settingsDialog.close());

    // ===== INIT =====
    isWorryTime = checkIsWorryTime();
    updateDoor();
    tick();
    setInterval(tick, 1000);
})();
