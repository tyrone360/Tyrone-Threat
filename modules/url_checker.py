from urllib.parse import urlsplit
import ipaddress


def analyze_url(url):
    """Analyse a URL for common warning signs without visiting it."""

    if not isinstance(url, str) or not url.strip():
        return {
            "success": False,
            "error": "Please enter a URL to analyse."
        }

    url = url.strip()

    if len(url) > 2048:
        return {
            "success": False,
            "error": "The URL is too long to analyse."
        }

    if any(char.isspace() for char in url):
        return {
            "success": False,
            "error": "The URL must not contain spaces."
        }

    try:
        parsed = urlsplit(url)

        scheme = parsed.scheme.lower()
        hostname = parsed.hostname

        if scheme not in ("http", "https"):
            return {
                "success": False,
                "error": "Only HTTP and HTTPS URLs are supported."
            }

        if not hostname:
            return {
                "success": False,
                "error": "The URL does not contain a valid hostname."
            }

        findings = []

        if scheme != "https":
            findings.append({
                "type": "warning",
                "message": "This URL does not use HTTPS encryption."
            })

        if parsed.username is not None or parsed.password is not None:
            findings.append({
                "type": "danger",
                "message": "The URL contains embedded login credentials."
            })

        try:
            ip_address = ipaddress.ip_address(hostname)

            findings.append({
                "type": "warning",
                "message": "The website uses an IP address instead of a domain name."
            })

            if not ip_address.is_global:
                findings.append({
                    "type": "warning",
                    "message": "The IP address is private, reserved, or local."
                })

        except ValueError:
            pass

        if "xn--" in hostname.lower():
            findings.append({
                "type": "warning",
                "message": "The domain contains an encoded internationalised name."
            })

        try:
            port = parsed.port

            if port is not None and port not in (80, 443):
                findings.append({
                    "type": "warning",
                    "message": f"The URL uses a non-standard web port: {port}."
                })

        except ValueError:
            return {
                "success": False,
                "error": "The URL contains an invalid port."
            }

        if len(url) > 200:
            findings.append({
                "type": "info",
                "message": "The URL is unusually long."
            })

        score = 0

        for finding in findings:
            if finding["type"] == "danger":
                score += 35
            elif finding["type"] == "warning":
                score += 20
            elif finding["type"] == "info":
                score += 5

        score = min(score, 100)

        if score >= 60:
            risk_level = "High"
        elif score >= 25:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        if not findings:
            findings.append({
                "type": "success",
                "message": "No common warning signs were detected."
            })

        return {
            "success": True,
            "url": url,
            "hostname": hostname,
            "risk_score": score,
            "risk_level": risk_level,
            "findings": findings,
            "recommendation": (
                "Avoid entering personal information until you have "
                "independently verified the website."
                if score >= 25
                else "Check that the domain belongs to the organisation "
                     "you intended to visit."
            ),
            "disclaimer": (
                "This is a basic URL indicator check, not a guarantee "
                "that a website is safe or malicious."
            )
        }

    except Exception:
        return {
            "success": False,
            "error": "The URL could not be analysed. Check the format."
        }
