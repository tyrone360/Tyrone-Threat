
def get_assistant_response(question):
    """
    Tyrone Threat - Local Cybersecurity Educational Assistant.

    Provides defensive cybersecurity awareness and safety guidance.
    This is a local rule-based assistant, not a generative AI model.
    """

    if not isinstance(question, str):
        return "Please enter a valid cybersecurity question."

    question = question.strip().lower()

    if not question:
        return "Please enter a question."

    if len(question) > 500:
        return "Your question is too long. Please keep it under 500 characters."

    # ==========================================
    # GREETINGS
    # ==========================================

    if any(word in question for word in [
        "hello", "hi", "hey", "good morning",
        "good afternoon", "good evening"
    ]):
        return (
            "WELCOME TO TYRONE AI\n\n"
            "Hello! I'm your Tyrone Threat cybersecurity learning assistant.\n\n"
            "I can help you understand:\n"
            "- Phishing and online scams\n"
            "- Malware and ransomware awareness\n"
            "- Password and account security\n"
            "- Website safety\n"
            "- Network security\n"
            "- Data protection\n"
            "- Digital privacy\n\n"
            "What would you like to learn about today?"
        )

    # ==========================================
    # PHISHING
    # ==========================================

    elif any(word in question for word in [
        "phishing", "fake email", "suspicious email",
        "scam", "fake message", "online fraud"
    ]):
        return (
            "PHISHING AWARENESS\n\n"
            "Phishing is online fraud where someone pretends to be "
            "a trusted organisation or person to trick people into "
            "revealing information.\n\n"
            "Warning signs:\n"
            "- Unexpected messages requesting personal information.\n"
            "- Suspicious links or attachments.\n"
            "- Messages creating unnecessary urgency.\n"
            "- Unusual sender addresses.\n"
            "- Offers that seem too good to be true.\n\n"
            "HOW TO STAY SAFE:\n"
            "- Avoid clicking unexpected links.\n"
            "- Verify the sender independently.\n"
            "- Never share passwords or verification codes.\n"
            "- Report suspicious messages.\n\n"
            "TIP: Contact the organisation through its official website."
        )

    # ==========================================
    # MALWARE
    # ==========================================

    elif any(word in question for word in [
        "malware", "virus", "ransomware", "trojan",
        "spyware", "computer infection"
    ]):
        return (
            "MALWARE AWARENESS\n\n"
            "Malware is software designed to harm devices, disrupt "
            "operations or access information without permission.\n\n"
            "Common types:\n"
            "- Virus: Malicious software that can spread between files.\n"
            "- Ransomware: Malware that can lock access to information.\n"
            "- Spyware: Software that secretly collects information.\n"
            "- Trojan: Malware disguised as legitimate software.\n\n"
            "PROTECTION:\n"
            "- Keep your operating system updated.\n"
            "- Use reputable security software.\n"
            "- Avoid unexpected downloads.\n"
            "- Back up important files.\n"
            "- Download software from trusted sources."
        )

    # ==========================================
    # HTTP AND HTTPS
    # ==========================================

    elif "https" in question or "http" in question:
        return (
            "HTTP VS HTTPS\n\n"
            "HTTP transfers information between a browser and a website.\n\n"
            "HTTPS adds encryption through TLS, helping protect "
            "information while it travels between your browser "
            "and the website.\n\n"
            "KEY DIFFERENCES:\n"
            "- HTTP does not provide HTTPS-style transport encryption.\n"
            "- HTTPS encrypts the connection using TLS.\n"
            "- HTTPS helps protect information from interception.\n\n"
            "IMPORTANT: HTTPS does not automatically mean a website "
            "is trustworthy. Fraudulent websites can also use HTTPS."
        )

    # ==========================================
    # WEBSITE SAFETY
    # ==========================================

    elif any(word in question for word in [
        "suspicious website", "unsafe website",
        "website safe", "trust a link", "url safety",
        "check a website", "fake website"
    ]):
        return (
            "WEBSITE SAFETY\n\n"
            "Before trusting a website:\n"
            "- Verify the domain name carefully.\n"
            "- Look for unusual spelling or extra characters.\n"
            "- Be cautious of unexpected redirects.\n"
            "- Check whether the website uses HTTPS.\n"
            "- Avoid entering personal information on unverified sites.\n"
            "- Use trusted security tools to check suspicious addresses.\n\n"
            "Remember: No single indicator proves that a website is safe."
        )

    # ==========================================
    # PASSWORD SECURITY
    # ==========================================

    elif any(word in question for word in [
        "password", "passphrase", "account security",
        "strong password", "password manager"
    ]):
        return (
            "PASSWORD SECURITY\n\n"
            "Strong account security helps prevent unauthorised access.\n\n"
            "RECOMMENDATIONS:\n"
            "- Use long, unique passwords.\n"
            "- Avoid reusing passwords across websites.\n"
            "- Use a reputable password manager.\n"
            "- Enable multi-factor authentication.\n"
            "- Never share verification codes.\n"
            "- Change compromised passwords promptly."
        )

    # ==========================================
    # MULTI-FACTOR AUTHENTICATION
    # ==========================================

    elif any(word in question for word in [
        "multi-factor", "multifactor", "two-factor",
        "2fa", "mfa", "verification code"
    ]):
        return (
            "MULTI-FACTOR AUTHENTICATION\n\n"
            "Multi-factor authentication (MFA) adds another "
            "security check when signing into an account.\n\n"
            "Examples include:\n"
            "- An authenticator application.\n"
            "- A security key.\n"
            "- A verification prompt on a trusted device.\n\n"
            "WHY IT MATTERS:\n"
            "Even if someone discovers your password, MFA can provide "
            "an additional layer of account protection.\n\n"
            "SAFETY TIP: Never approve an unexpected login request "
            "or share your verification codes."
        )

    # ==========================================
    # DATA BREACHES
    # ==========================================

    elif any(word in question for word in [
        "data breach", "leaked data", "data leak",
        "personal information exposed"
    ]):
        return (
            "DATA BREACH AWARENESS\n\n"
            "A data breach occurs when information is accessed "
            "or disclosed without proper authorisation.\n\n"
            "Protect yourself by:\n"
            "- Using unique passwords.\n"
            "- Enabling multi-factor authentication.\n"
            "- Monitoring important accounts.\n"
            "- Being cautious about unexpected messages.\n"
            "- Checking official notifications from affected services.\n\n"
            "If an account is affected, change its password using "
            "the official website and review its security settings."
        )

    # ==========================================
    # FIREWALLS
    # ==========================================

    elif "firewall" in question:
        return (
            "FIREWALL AWARENESS\n\n"
            "A firewall is a security control that monitors and "
            "filters network traffic according to configured rules.\n\n"
            "WHY FIREWALLS MATTER:\n"
            "- Help control network connections.\n"
            "- Reduce unwanted network access.\n"
            "- Support an organisation's security policies.\n\n"
            "BEST PRACTICES:\n"
            "- Keep your device firewall enabled.\n"
            "- Use trusted network security settings.\n"
            "- Review security notifications.\n"
            "- Ask an administrator before changing managed settings."
        )

    # ==========================================
    # WI-FI AND NETWORK SECURITY
    # ==========================================

    elif any(word in question for word in [
        "wifi", "wi-fi", "wireless network",
        "public network", "public wifi", "network security"
    ]):
        return (
            "NETWORK SECURITY\n\n"
            "Network security helps protect devices and information "
            "communicated across connected systems.\n\n"
            "SAFETY RECOMMENDATIONS:\n"
            "- Secure your home Wi-Fi with a strong password.\n"
            "- Use modern router security settings.\n"
            "- Keep router firmware updated.\n"
            "- Avoid sensitive activities on untrusted public networks.\n"
            "- Turn off automatic connection to unknown networks.\n"
            "- Use HTTPS websites.\n\n"
            "TIP: Do not assume a network is trustworthy just because "
            "it has a familiar name."
        )

    # ==========================================
    # SOFTWARE UPDATES
    # ==========================================

    elif any(word in question for word in [
        "software update", "system update",
        "security update", "patch", "outdated software"
    ]):
        return (
            "SOFTWARE UPDATE AWARENESS\n\n"
            "Software updates can fix security weaknesses, improve "
            "performance and correct software problems.\n\n"
            "RECOMMENDATIONS:\n"
            "- Enable automatic security updates where appropriate.\n"
            "- Update your operating system.\n"
            "- Keep your browser updated.\n"
            "- Update applications from official sources.\n"
            "- Restart devices when required to complete updates.\n\n"
            "TIP: Avoid unofficial update files and unexpected update links."
        )

    # ==========================================
    # BACKUPS
    # ==========================================

    elif any(word in question for word in [
        "backup", "backups", "recover files",
        "data recovery", "protect my files"
    ]):
        return (
            "DATA BACKUP AWARENESS\n\n"
            "A backup is an additional copy of important information "
            "that can help restore files after accidental loss or "
            "a security incident.\n\n"
            "GOOD PRACTICES:\n"
            "- Back up important files regularly.\n"
            "- Keep a separate backup copy.\n"
            "- Protect backups with appropriate access controls.\n"
            "- Test whether your backups can be restored.\n"
            "- Keep backup software updated.\n\n"
            "TIP: A backup is useful only if it is available and can "
            "be restored when needed."
        )

    # ==========================================
    # SOCIAL ENGINEERING
    # ==========================================

    elif any(word in question for word in [
        "social engineering", "manipulation",
        "impersonation", "identity fraud"
    ]):
        return (
            "SOCIAL ENGINEERING AWARENESS\n\n"
            "Social engineering involves manipulating people into "
            "sharing information or taking actions that could "
            "compromise security.\n\n"
            "WARNING SIGNS:\n"
            "- Someone pretending to be technical support.\n"
            "- Unexpected requests for passwords.\n"
            "- Pressure to act immediately.\n"
            "- Requests to bypass normal security procedures.\n\n"
            "PROTECTION:\n"
            "- Verify someone's identity independently.\n"
            "- Never share login credentials.\n"
            "- Follow official security procedures.\n"
            "- Report suspicious requests."
        )

    # ==========================================
    # SECURITY AWARENESS
    # ==========================================

    elif any(word in question for word in [
        "online scam", "online scams",
        "identity theft", "safe online shopping",
        "online shopping safety", "suspicious login",
        "login notification", "protect personal information",
        "personal information safety"
    ]):
        return (
            "SECURITY AWARENESS\n\n"
            "Security awareness helps people recognise online risks "
            "and make safer decisions when using digital services.\n\n"
            "IMPORTANT SAFETY RECOMMENDATIONS:\n"
            "- Be cautious of unexpected offers and online messages.\n"
            "- Verify sellers before making online purchases.\n"
            "- Never share passwords or verification codes.\n"
            "- Review unexpected login notifications carefully.\n"
            "- Use official websites and applications.\n"
            "- Avoid sharing unnecessary personal information.\n"
            "- Enable multi-factor authentication.\n"
            "- Report suspicious activity to the relevant service provider.\n\n"
            "IDENTITY THEFT AWARENESS:\n"
            "Identity theft involves someone using another person's "
            "personal information without permission.\n\n"
            "TIP: Stop and verify unexpected requests before sharing "
            "information or making payments."
        )

    # ==========================================
    # DIGITAL PRIVACY
    # ==========================================

    elif any(word in question for word in [
        "privacy", "personal data", "online tracking",
        "digital footprint", "protect my information"
    ]):
        return (
            "DIGITAL PRIVACY\n\n"
            "Digital privacy concerns how personal information "
            "is collected, stored, shared and used online.\n\n"
            "PROTECT YOUR PRIVACY:\n"
            "- Review application permissions.\n"
            "- Limit unnecessary personal information sharing.\n"
            "- Use privacy settings on social platforms.\n"
            "- Be careful with public posts.\n"
            "- Review website privacy policies.\n"
            "- Use unique passwords and MFA.\n\n"
            "TIP: Think carefully before sharing personal information online."
        )

    # ==========================================
    # SECURITY INCIDENT RESPONSE
    # ==========================================

    elif any(word in question for word in [
        "hacked", "account compromised",
        "security incident", "device compromised",
        "someone accessed my account"
    ]):
        return (
            "SECURITY INCIDENT GUIDANCE\n\n"
            "If you believe an account or device has been compromised:\n\n"
            "1. Stop interacting with suspicious messages or links.\n"
            "2. Use a trusted device to access the official account website.\n"
            "3. Change affected passwords.\n"
            "4. Enable multi-factor authentication.\n"
            "5. Review recent account activity and active sessions.\n"
            "6. Contact the relevant service provider or IT administrator.\n"
            "7. Preserve relevant notifications for investigation.\n\n"
            "If this involves a school or workplace device, report "
            "the incident to the responsible IT team."
        )

    # ==========================================
    # GENERAL CYBERSECURITY
    # ==========================================

    elif any(word in question for word in [
        "cybersecurity", "cyber security",
        "protect my computer", "stay safe online",
        "online safety", "digital security"
    ]):
        return (
            "CYBERSECURITY BASICS\n\n"
            "Cybersecurity protects devices, systems, accounts "
            "and information from digital threats.\n\n"
            "IMPORTANT SECURITY HABITS:\n"
            "- Install software updates.\n"
            "- Use unique passwords.\n"
            "- Enable multi-factor authentication.\n"
            "- Back up important information.\n"
            "- Avoid suspicious links and attachments.\n"
            "- Use reputable security software.\n"
            "- Protect personal information.\n"
            "- Report suspicious activity."
        )

    # ==========================================
    # THANK YOU
    # ==========================================

    elif any(word in question for word in [
        "thank you", "thanks", "appreciate it"
    ]):
        return (
            "YOU'RE WELCOME!\n\n"
            "Stay informed, stay alert and practise good "
            "cybersecurity habits.\n\n"
            "Tyrone Threat - Building a safer digital environment."
        )

    # ==========================================
    # HELP
    # ==========================================

    elif "help" in question or "what can you do" in question:
        return (
            "TYRONE AI - AVAILABLE TOPICS\n\n"
            "I can help explain:\n"
            "- Phishing and online scams.\n"
            "- Malware and ransomware awareness.\n"
            "- HTTP and HTTPS.\n"
            "- Suspicious website indicators.\n"
            "- Password security.\n"
            "- Multi-factor authentication.\n"
            "- Data breaches.\n"
            "- Firewalls.\n"
            "- Wi-Fi and network security.\n"
            "- Software updates.\n"
            "- Data backups.\n"
            "- Social engineering.\n"
            "- Digital privacy.\n"
            "- Security incident response.\n\n"
            "Ask me a question about any of these topics!"
        )

    # ==========================================
    # PASSWORD AND ACCOUNT SECURITY
    # ==========================================

    elif any(word in question for word in [
        "password", "passphrase", "account security",
        "strong password", "password manager",
        "protect my accounts", "secure my accounts",
        "protect my account", "secure my account",
        "hackers", "protect my online accounts"
    ]):
        return (
            "ACCOUNT AND PASSWORD SECURITY\n\n"
            "Protecting your online accounts helps prevent "
            "unauthorised access.\n\n"
            "SAFETY RECOMMENDATIONS:\n"
            "- Use a unique, strong password for every account.\n"
            "- Enable multi-factor authentication (MFA).\n"
            "- Never share passwords or verification codes.\n"
            "- Be careful with suspicious emails and login links.\n"
            "- Review your account login activity regularly.\n"
            "- Keep devices and applications updated.\n"
            "- Use official websites and applications when signing in.\n\n"
            "TIP: Never approve a login request that you did not initiate."
        )
    # ==========================================
    # DEFAULT RESPONSE
    # ==========================================

    else:
        return (
            "TYRONE AI - CYBERSECURITY ASSISTANT\n\n"
            "Thanks for your question!\n\n"
            "I may not have a prepared answer for that topic yet.\n\n"
            "Try asking about:\n"
            "- What is phishing?\n"
            "- How do I protect my computer from malware?\n"
            "- What is multi-factor authentication?\n"
            "- Why are firewalls important?\n"
            "- How can I secure my Wi-Fi?\n"
            "- What is a data breach?\n"
            "- How do I protect my online privacy?\n\n"
            "I'm designed to provide educational and defensive "
            "cybersecurity guidance."
        )
