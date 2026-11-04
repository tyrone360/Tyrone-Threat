
document.addEventListener("DOMContentLoaded", () => {

    // ==========================================
    // DASHBOARD
    // ==========================================

    async function loadDashboard() {
        try {
            const response = await fetch("/api/dashboard");

            if (!response.ok) {
                throw new Error("Dashboard request failed");
            }

            const data = await response.json();

            const threatCount = document.getElementById("threat-count");
            const alertCount = document.getElementById("alert-count");
            const systemCount = document.getElementById("system-count");
            const healthStatus = document.getElementById("health-status");
            const backendStatus = document.getElementById("backend-status");

            if (threatCount) threatCount.textContent = data.threats_detected;
            if (alertCount) alertCount.textContent = data.security_alerts;
            if (systemCount) systemCount.textContent = data.protected_systems;
            if (healthStatus) healthStatus.textContent = data.system_health;
            if (backendStatus) backendStatus.textContent = "Connected";

        } catch (error) {
            console.error("Dashboard error:", error);

            const healthStatus = document.getElementById("health-status");
            const backendStatus = document.getElementById("backend-status");

            if (healthStatus) healthStatus.textContent = "Unavailable";
            if (backendStatus) backendStatus.textContent = "Disconnected";
        }
    }


    // ==========================================
    // CURRENT DATE
    // ==========================================

    const dateElement = document.getElementById("current-date");

    if (dateElement) {
        dateElement.textContent = new Date().toLocaleDateString("en-ZA", {
            weekday: "short",
            year: "numeric",
            month: "short",
            day: "numeric"
        });
    }


    // ==========================================
    // MOBILE SIDEBAR
    // ==========================================

    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.getElementById("sidebar");

    if (menuToggle && sidebar) {
        menuToggle.addEventListener("click", () => {
            sidebar.classList.toggle("open");
        });
    }

    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", () => {

            document.querySelectorAll(".nav-link").forEach(item => {
                item.classList.remove("active");
            });

            link.classList.add("active");

            if (sidebar) {
                sidebar.classList.remove("open");
            }
        });
    });


    // ==========================================
    // URL SAFETY SCANNER
    // ==========================================

    const urlForm = document.getElementById("url-check-form");
    const urlInput = document.getElementById("url-input");
    const scanButton = document.getElementById("scan-url-button");

    const loadingPanel = document.getElementById("scanner-loading");
    const errorPanel = document.getElementById("scanner-error");
    const resultsPanel = document.getElementById("scanner-results");

    if (urlForm && urlInput && scanButton) {

        urlForm.addEventListener("submit", async (event) => {

            event.preventDefault();

            const url = urlInput.value.trim();

            if (!url) {
                showScannerError("Please enter a website address.");
                return;
            }

            if (errorPanel) {
                errorPanel.hidden = true;
                errorPanel.textContent = "";
            }

            if (resultsPanel) {
                resultsPanel.hidden = true;
            }

            if (loadingPanel) {
                loadingPanel.hidden = false;
            }

            scanButton.disabled = true;
            scanButton.textContent = "Analysing...";

            try {

                const response = await fetch("/api/check-url", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ url: url })
                });

                const data = await response.json();

                if (!response.ok || !data.success) {
                    throw new Error(data.error || "Unable to analyse this URL.");
                }

                displayScannerResults(data);

            } catch (error) {

                console.error("URL scanner error:", error);

                showScannerError(
                    error.message || "Something went wrong. Please try again."
                );

            } finally {

                if (loadingPanel) {
                    loadingPanel.hidden = true;
                }

                scanButton.disabled = false;
                scanButton.textContent = "Analyse URL";

                if (window.lucide) {
                    window.lucide.createIcons();
                }
            }
        });
    }


    // ==========================================
    // DISPLAY SCANNER ERROR
    // ==========================================

    function showScannerError(message) {

        if (!errorPanel) return;

        errorPanel.textContent = message;
        errorPanel.hidden = false;
    }


    // ==========================================
    // DISPLAY SCANNER RESULTS
    // ==========================================

    function displayScannerResults(data) {

        if (!resultsPanel) return;

        const score = Number(data.risk_score) || 0;
        const riskLevel = String(data.risk_level || "Low").toLowerCase();
        const findings = Array.isArray(data.findings) ? data.findings : [];

        const riskBadge = document.getElementById("risk-badge");
        const scoreElement = document.getElementById("risk-score");
        const scoreCircle = document.getElementById("risk-score-circle");

        const hostnameElement = document.getElementById("result-hostname");
        const summaryElement = document.getElementById("result-summary-text");

        const findingCount = document.getElementById("finding-count");
        const findingsList = document.getElementById("findings-list");

        const recommendation = document.getElementById("recommendation-text");
        const disclaimer = document.getElementById("scanner-disclaimer");

        if (riskBadge) {
            riskBadge.textContent = `${riskLevel.toUpperCase()} RISK`;
            riskBadge.className = `risk-badge ${riskLevel}`;
        }

        if (scoreElement) {
            scoreElement.textContent = score;
        }

        if (scoreCircle) {
            scoreCircle.className = `risk-score-circle ${riskLevel}`;
        }

        if (hostnameElement) {
            hostnameElement.textContent = data.hostname || "Unknown domain";
        }

        if (summaryElement) {
            summaryElement.textContent = findings.length === 0
                ? "No common warning indicators were identified by this basic check."
                : `${findings.length} indicator(s) were identified and may need attention.`;
        }

        if (findingCount) {
            findingCount.textContent =
                `${findings.length} FINDING${findings.length === 1 ? "" : "S"}`;
        }

        if (findingsList) {

            findingsList.replaceChildren();

            if (findings.length === 0) {

                const emptyMessage = document.createElement("p");
                emptyMessage.className = "finding-item success";
                emptyMessage.textContent = "No common warning indicators were identified.";
                findingsList.appendChild(emptyMessage);

            } else {

                findings.forEach(finding => {

                    const item = document.createElement("div");
                    const type = String(finding.type || "info").toLowerCase();

                    const allowedTypes = ["danger", "warning", "info", "success"];
                    const safeType = allowedTypes.includes(type) ? type : "info";

                    item.className = `finding-item ${safeType}`;

                    const icon = document.createElement("i");
                    icon.setAttribute("data-lucide", getFindingIcon(safeType));

                    const message = document.createElement("span");
                    message.textContent = finding.message || "An indicator was detected.";

                    item.appendChild(icon);
                    item.appendChild(message);

                    findingsList.appendChild(item);
                });
            }
        }

        if (recommendation) {
            recommendation.textContent =
                data.recommendation || "Verify the website address before interacting with it.";
        }

        if (disclaimer) {
            disclaimer.textContent =
                data.disclaimer ||
                "This basic indicator check cannot guarantee that a website is safe or malicious.";
        }

        resultsPanel.hidden = false;
        loadScanHistory();

        if (window.lucide) {
            window.lucide.createIcons();
        }
    }


    // ==========================================
    // FINDING ICONS
    // ==========================================

    function getFindingIcon(type) {

        const icons = {
            danger: "alert-triangle",
            warning: "alert-circle",
            info: "info",
            success: "shield-check"
        };

        return icons[type] || "info";
    }


    // ==========================================
    // SCAN HISTORY
    // ==========================================

    async function loadScanHistory() {

        const tableBody = document.getElementById("history-table-body");
        const totalElement = document.getElementById("history-total");

        if (!tableBody) return;

        try {

            const response = await fetch("/api/history");

            if (!response.ok) {
                throw new Error("Unable to retrieve scan history.");
            }

            const data = await response.json();
            const history = data.history || [];

            tableBody.replaceChildren();

            if (totalElement) {
                totalElement.textContent =
                    `${data.total} saved scan${data.total === 1 ? "" : "s"}`;
            }

            if (history.length === 0) {
                const row = document.createElement("tr");
                const cell = document.createElement("td");

                cell.colSpan = 4;
                cell.textContent = "No previous scans found.";

                row.appendChild(cell);
                tableBody.appendChild(row);
                return;
            }

            history.forEach(scan => {

                const row = document.createElement("tr");

                const website = document.createElement("td");
                website.textContent = scan.hostname || "Unknown";

                const score = document.createElement("td");
                score.textContent = scan.risk_score;

                const riskCell = document.createElement("td");
                const badge = document.createElement("span");

                const risk = String(scan.risk_level || "low").toLowerCase();

                badge.className = `history-risk ${risk}`;
                badge.textContent = risk.toUpperCase();

                riskCell.appendChild(badge);

                const date = document.createElement("td");
                const parsedDate = new Date(scan.created_at);

                date.textContent = Number.isNaN(parsedDate.getTime())
                    ? "Unknown date"
                    : parsedDate.toLocaleString("en-ZA");

                row.append(website, score, riskCell, date);
                tableBody.appendChild(row);
            });

        } catch (error) {

            console.error("History error:", error);

            tableBody.replaceChildren();

            const row = document.createElement("tr");
            const cell = document.createElement("td");

            cell.colSpan = 4;
            cell.textContent = "Unable to load scan history.";

            row.appendChild(cell);
            tableBody.appendChild(row);
        }
    }


    const refreshHistoryButton = document.getElementById("refresh-history");

    if (refreshHistoryButton) {
        refreshHistoryButton.addEventListener("click", loadScanHistory);
    }


    // ==========================================
    // LIVE SECURITY MONITORING
    // ==========================================

    async function loadSecurityMonitoring() {

        const statusText = document.getElementById("monitoring-status-text");
        const statusIndicator = document.getElementById("monitoring-status-indicator");

        try {

            const response = await fetch("/api/monitoring");

            if (!response.ok) {
                throw new Error("Monitoring API is unavailable.");
            }

            const data = await response.json();

            const backendElement = document.getElementById("monitor-backend-status");

            if (backendElement) {
                backendElement.textContent =
                    data.status === "online" ? "ONLINE" : "OFFLINE";
            }

            if (statusText) statusText.textContent = "Monitoring Active";

            if (statusIndicator) {
                statusIndicator.className = "status-indicator online";
            }

            const totalSeconds = data.uptime_seconds || 0;
            const hours = Math.floor(totalSeconds / 3600);
            const minutes = Math.floor((totalSeconds % 3600) / 60);
            const seconds = totalSeconds % 60;

            const uptimeElement = document.getElementById("monitor-uptime");

            if (uptimeElement) {
                uptimeElement.textContent = `${hours}h ${minutes}m ${seconds}s`;
            }

            const metrics = data.metrics || {};

            const metricElements = {
                "monitor-total-scans": metrics.total_scans || 0,
                "monitor-low-risk": metrics.low_risk || 0,
                "monitor-medium-risk": metrics.medium_risk || 0,
                "monitor-high-risk": metrics.high_risk || 0
            };

            Object.entries(metricElements).forEach(([id, value]) => {
                const element = document.getElementById(id);
                if (element) element.textContent = value;
            });

            const activityContainer =
                document.getElementById("monitoring-activity-list");

            if (activityContainer) {

                activityContainer.replaceChildren();

                const activities = data.recent_activity || [];

                if (activities.length === 0) {

                    const emptyMessage = document.createElement("p");
                    emptyMessage.className = "monitor-empty";
                    emptyMessage.textContent = "No security activity recorded yet.";

                    activityContainer.appendChild(emptyMessage);

                } else {

                    activities.forEach(activity => {

                        const item = document.createElement("div");
                        item.className = "monitor-activity-item";

                        const info = document.createElement("div");
                        info.className = "monitor-activity-info";

                        const hostname = document.createElement("strong");
                        hostname.textContent = activity.hostname || "Unknown host";

                        const details = document.createElement("span");
                        details.textContent =
                            `${activity.url} • Score: ${activity.risk_score}`;

                        const risk = document.createElement("span");
                        const riskLevel = (activity.risk_level || "low").toLowerCase();

                        risk.className = `monitor-risk ${
                            ["low", "medium", "high"].includes(riskLevel)
                                ? riskLevel
                                : "low"
                        }`;

                        risk.textContent = activity.risk_level || "Unknown";

                        info.appendChild(hostname);
                        info.appendChild(details);

                        item.appendChild(info);
                        item.appendChild(risk);

                        activityContainer.appendChild(item);
                    });
                }
            }

            const updatedElement = document.getElementById("monitor-last-updated");

            if (updatedElement) {
                updatedElement.textContent =
                    "Updated: " + new Date(data.checked_at).toLocaleTimeString();
            }

        } catch (error) {

            console.error("Monitoring error:", error);

            const backendElement = document.getElementById("monitor-backend-status");

            if (backendElement) backendElement.textContent = "OFFLINE";
            if (statusText) statusText.textContent = "Connection Lost";

            if (statusIndicator) {
                statusIndicator.className = "status-indicator offline";
            }
        }
    }


    // ==========================================
    // SECURITY REPORTS
    // ==========================================

    async function loadSecurityReport() {

        try {

            const response = await fetch("/api/monitoring");

            if (!response.ok) {
                throw new Error("Could not load security report.");
            }

            const data = await response.json();
            const metrics = data.metrics || {};

            const total = Number(metrics.total_scans) || 0;
            const low = Number(metrics.low_risk) || 0;
            const medium = Number(metrics.medium_risk) || 0;
            const high = Number(metrics.high_risk) || 0;

            const reportValues = {
                "report-total-scans": total,
                "report-low-risk": low,
                "report-medium-risk": medium,
                "report-high-risk": high
            };

            Object.entries(reportValues).forEach(([id, value]) => {
                const element = document.getElementById(id);
                if (element) element.textContent = value;
            });

            const percentage = value =>
                total > 0 ? Math.round((value / total) * 100) : 0;

            const percentages = {
                "report-low-percentage": percentage(low),
                "report-medium-percentage": percentage(medium),
                "report-high-percentage": percentage(high)
            };

            Object.entries(percentages).forEach(([id, value]) => {
                const element = document.getElementById(id);
                if (element) element.textContent = `${value}%`;
            });

            const bars = {
                "report-low-bar": percentage(low),
                "report-medium-bar": percentage(medium),
                "report-high-bar": percentage(high)
            };

            Object.entries(bars).forEach(([id, value]) => {
                const element = document.getElementById(id);
                if (element) element.style.width = `${value}%`;
            });

            const generatedDate = document.getElementById("report-generated-date");

            if (generatedDate) {
                generatedDate.textContent =
                    "Generated: " + new Date(data.checked_at).toLocaleString();
            }

        } catch (error) {

            console.error("Security report error:", error);

            const generatedDate = document.getElementById("report-generated-date");

            if (generatedDate) {
                generatedDate.textContent =
                    "Unable to load report data. Check your backend connection.";
            }
        }
    }


    const refreshReportButton =
        document.getElementById("refresh-security-report");

    if (refreshReportButton) {
        refreshReportButton.addEventListener("click", loadSecurityReport);
    }


    // ==========================================
    // TYRONE THREAT SECURITY ASSISTANT
    // ==========================================

    const assistantForm = document.getElementById("assistant-form");
    const assistantInput = document.getElementById("assistant-input");
    const assistantChat = document.getElementById("assistant-chat");
    const assistantSend = document.getElementById("assistant-send");

    function addChatMessage(role, message) {

        if (!assistantChat) return null;

        const messageContainer = document.createElement("div");

        messageContainer.className =
            role === "user"
                ? "chat-message user-message"
                : "chat-message assistant-message";

        const avatar = document.createElement("div");
        avatar.className =
            role === "user" ? "chat-avatar user-avatar" : "chat-avatar";

        avatar.textContent = role === "user" ? "YOU" : "TT";

        const bubble = document.createElement("div");
        bubble.className = "chat-bubble";
        bubble.textContent = message;

        messageContainer.appendChild(avatar);
        messageContainer.appendChild(bubble);

        assistantChat.appendChild(messageContainer);

        assistantChat.scrollTop = assistantChat.scrollHeight;

        return bubble;
    }


    async function askAssistant(question) {

        const cleanQuestion = String(question || "").trim();

        if (!cleanQuestion) return;

        if (cleanQuestion.length > 500) {
            addChatMessage("assistant", "Please keep your question under 500 characters.");
            return;
        }

        if (!assistantChat) {
            console.error("Assistant chat container was not found.");
            return;
        }

        addChatMessage("user", cleanQuestion);

        const loadingBubble = addChatMessage(
            "assistant",
            "Preparing your security awareness response..."
        );

        if (assistantSend) {
            assistantSend.disabled = true;
            assistantSend.textContent = "Sending...";
        }

        if (assistantInput) {
            assistantInput.disabled = true;
        }

        try {

            const response = await fetch("/api/assistant", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: cleanQuestion
                })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || "The assistant could not respond.");
            }

            if (loadingBubble) {
                loadingBubble.textContent =
                    data.answer || "No response was returned.";
            }

        } catch (error) {

            console.error("Assistant error:", error);

            if (loadingBubble) {
                loadingBubble.textContent =
                    "Sorry, I could not connect to the security assistant. Please try again.";
            }

        } finally {

            if (assistantSend) {
                assistantSend.disabled = false;
                assistantSend.textContent = "Send";
            }

            if (assistantInput) {
                assistantInput.disabled = false;
                assistantInput.focus();
            }

            if (assistantChat) {
                assistantChat.scrollTop = assistantChat.scrollHeight;
            }
        }
    }


    // Submit a question using the form

    if (assistantForm && assistantInput) {

        assistantForm.addEventListener("submit", async (event) => {

            event.preventDefault();

            const question = assistantInput.value.trim();

            if (!question) return;

            assistantInput.value = "";

            await askAssistant(question);
        });
    }


    // Suggested question buttons

    document.querySelectorAll(".suggestion-btn").forEach(button => {

        button.addEventListener("click", async () => {

            const question = button.dataset.question;

            if (!question) return;

            if (assistantInput) {
                assistantInput.value = question;
            }

            await askAssistant(question);
        });
    });


    // ==========================================
    // INITIALISE DASHBOARD FEATURES
    // ==========================================

    if (window.lucide) {
        window.lucide.createIcons();
    }

    loadDashboard();
    loadScanHistory();
    loadSecurityMonitoring();
    loadSecurityReport();

    // Refresh monitoring data every 15 seconds
    setInterval(loadSecurityMonitoring, 15000);

});

// ==========================================
// TYRONE THREAT - CYBERSECURITY QUIZ
// ==========================================

const quizQuestions = [
    {
        question: "What does HTTPS help protect?",
        options: [
            "The physical computer",
            "Information transferred between browser and website",
            "The website owner's password",
            "The computer battery"
        ],
        answer: 1,
        explanation: "HTTPS uses encryption to help protect information during transmission."
    },
    {
        question: "What is phishing?",
        options: [
            "A computer cleaning process",
            "A type of internet connection",
            "An attempt to trick people into revealing information",
            "A software update"
        ],
        answer: 2,
        explanation: "Phishing uses deceptive messages or websites to trick people into sharing information."
    },
    {
        question: "Why is multi-factor authentication important?",
        options: [
            "It makes your internet faster",
            "It adds another layer of account protection",
            "It removes all computer viruses",
            "It increases screen brightness"
        ],
        answer: 1,
        explanation: "MFA adds another verification step when signing into an account."
    },
    {
        question: "What is the main purpose of a firewall?",
        options: [
            "To charge a computer",
            "To improve screen resolution",
            "To monitor and filter network traffic",
            "To create social media accounts"
        ],
        answer: 2,
        explanation: "A firewall monitors and filters network traffic according to security rules."
    },
    {
        question: "What should you do when you receive a suspicious email?",
        options: [
            "Click every link",
            "Share your password",
            "Download every attachment",
            "Verify the sender and avoid unexpected links"
        ],
        answer: 3,
        explanation: "Always verify suspicious messages independently before taking action."
    }
];

let currentQuestion = 0;
let quizScore = 0;
let answerSelected = false;

function loadQuizQuestion() {
    const question = quizQuestions[currentQuestion];

    document.getElementById("quiz-question").textContent =
        question.question;

    document.getElementById("quiz-progress").textContent =
        `Question ${currentQuestion + 1} of ${quizQuestions.length}`;

    document.getElementById("quiz-score").textContent =
        `Score: ${quizScore}`;

    document.getElementById("quiz-progress-fill").style.width =
        `${((currentQuestion + 1) / quizQuestions.length) * 100}%`;

    const optionsContainer = document.getElementById("quiz-options");
    optionsContainer.innerHTML = "";

    question.options.forEach((option, index) => {
        const button = document.createElement("button");

        button.className = "quiz-option";
        button.textContent = option;

        button.addEventListener("click", () => {
            selectQuizAnswer(index);
        });

        optionsContainer.appendChild(button);
    });

    document.getElementById("quiz-feedback").textContent = "";

    document.getElementById("quiz-next").disabled = true;
    document.getElementById("quiz-next").textContent =
        currentQuestion === quizQuestions.length - 1
            ? "View Results"
            : "Next Question";

    document.getElementById("quiz-next").hidden = false;
    document.getElementById("quiz-restart").hidden = true;

    answerSelected = false;
}

function selectQuizAnswer(selectedIndex) {
    if (answerSelected) return;

    answerSelected = true;

    const question = quizQuestions[currentQuestion];
    const buttons = document.querySelectorAll(".quiz-option");

    buttons.forEach((button, index) => {
        button.disabled = true;

        if (index === question.answer) {
            button.classList.add("correct");
        }

        if (index === selectedIndex && index !== question.answer) {
            button.classList.add("incorrect");
        }
    });

    const feedback = document.getElementById("quiz-feedback");

    if (selectedIndex === question.answer) {
        quizScore++;

        feedback.textContent =
            "Correct! " + question.explanation;
    } else {
        feedback.textContent =
            "Not quite. " + question.explanation;
    }

    document.getElementById("quiz-score").textContent =
        `Score: ${quizScore}`;

    document.getElementById("quiz-next").disabled = false;
}

function nextQuizQuestion() {
    if (!answerSelected) return;

    if (currentQuestion < quizQuestions.length - 1) {
        currentQuestion++;
        loadQuizQuestion();
    } else {
        showQuizResults();
    }
}

function showQuizResults() {
    document.getElementById("quiz-question").textContent =
        "Quiz Completed!";

    document.getElementById("quiz-options").innerHTML = "";

    document.getElementById("quiz-progress").textContent =
        "Assessment complete";

    document.getElementById("quiz-progress-fill").style.width = "100%";

    document.getElementById("quiz-next").hidden = true;

    document.getElementById("quiz-feedback").textContent =
        `You scored ${quizScore} out of ${quizQuestions.length}. ` +
        (quizScore === 5
            ? "Excellent work! You have strong cybersecurity awareness."
            : quizScore >= 3
                ? "Good effort! Keep learning and improving your security knowledge."
                : "Keep practising! Review the cybersecurity awareness topics and try again.");

    document.getElementById("quiz-restart").hidden = false;
}

function restartQuiz() {
    currentQuestion = 0;
    quizScore = 0;
    answerSelected = false;

    loadQuizQuestion();
}

document.addEventListener("DOMContentLoaded", () => {
    const nextButton = document.getElementById("quiz-next");
    const restartButton = document.getElementById("quiz-restart");

    if (nextButton && restartButton) {
        nextButton.addEventListener("click", nextQuizQuestion);
        restartButton.addEventListener("click", restartQuiz);

        loadQuizQuestion();
    }
});
