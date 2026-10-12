"""
Single registry of every tool in the suite. Dashboard cards, sidebar navigation,
per-user access control (admin panel) and the "coming soon" pages all read from here.

status:  live      -> working in this build
         soon      -> planned (phase says when)
         external  -> separate deployment, opened in a new tab (own login)
"""

GROUPS = ["Reports", "Communication", "Lookup & Automation", "Other apps", "Administration"]

PTP_MODES = [
    ("dashboard", "Overview"),
    ("monthwise", "Month-wise Report"),
    ("topaygen", "Generate ToPay Report"),
    ("paidgen", "Generate Paid Report"),
    ("combinedgen", "Paid & ToPay Report"),
    ("regionwise", "Region-wise Report"),
    ("automail", "Auto Mail (Region-wise)"),
    ("cnquery", "CN Query Tool"),
]

MODULES = [
    dict(id="paid_topay", name="Paid / ToPay Suite", icon="chart", group="Reports", status="live",
         endpoint="paid_topay.index",
         desc="Month-wise B.CODE report, ToPay/Paid report generators, region split, auto mail aur CN query.",
         children=PTP_MODES),
    dict(id="dbp_report", name="DBP Report Builder", icon="file", group="Reports", status="soon", phase=2,
         desc="Excel exports upload karo, branch-wise DBP report (SUMMARY, PAID, TO PAY, PENDING BILLING, DDR...) banao.",
         planned=["Report Builder (one row per normalized B.CODE, duplicate protection)",
                  "DDR branch resolution with DDR AUDIT sheet",
                  "Customer / audit tabs (BOSCH, TATA MOTORS, APTIV, OTHER END, DISPUTE...)"]),
    dict(id="month_summary", name="Month-wise Summary (ADR)", icon="calendar", group="Reports", status="soon", phase=2,
         desc="ADR (Pending Billing) raw data se branch x month pending matrix.",
         planned=["ADR raw upload", "Branch x month pending matrix", "Excel export"]),
    dict(id="ai_chatbot", name="AI Chatbot", icon="bot", group="Reports", status="soon", phase=2,
         desc="Loaded report data se seedha sawaal-jawaab (numbers hamesha data se, AI se nahi).",
         planned=["'801 ki pending batao', 'branch wise DDR pending'", "Gemini sirf wording ke liye (optional)"]),
    dict(id="validation", name="Validation & Audit", icon="check", group="Reports", status="soon", phase=2,
         desc="Duplicate/missing branch, DDR resolution aur reconciliation checks.",
         planned=["Duplicate dockets / branch codes", "Unknown branches", "DDR resolution audit"]),
    dict(id="mail_center", name="Mail Center", icon="mail", group="Communication", status="soon", phase=2,
         desc="Branch-wise verified pending mails, region auto-mail aur Thunderbird/SMTP sending.",
         planned=["Verified To/CC/Subject/body + .eml draft", "Auto Mail - All Region (test mode default ON)",
                  "Send Full DBP Report", "One merged Thunderbird extension"]),
    dict(id="tbb_mail", name="TBB Party Mail", icon="mail", group="Communication", status="soon", phase=3,
         desc="Branch-wise GR verification mail."),
    dict(id="bill_mail", name="Bill Generated Mail", icon="mail", group="Communication", status="soon", phase=3,
         desc="Branch-wise Auto Generated Freight Bill mail."),
    dict(id="branch_finder", name="Branch Detail Finder", icon="building", group="Lookup & Automation",
         status="soon", phase=3, desc="Branch code lookup (single + bulk Excel)."),
    dict(id="customer_search", name="Customer Search", icon="search", group="Lookup & Automation",
         status="soon", phase=3, desc="Customer search (manual + bulk Excel)."),
    dict(id="om_automation", name="OM Automation", icon="truck", group="Lookup & Automation",
         status="soon", phase=3, desc="CN / GST / Party Code / Master lookup (GST Query needs Chrome - Docker deploy)."),
    dict(id="gr_auto", name="GR Auto Modification", icon="link", group="Other apps", status="external",
         desc="Separate app with its own login - opens in a new tab."),
    dict(id="directory", name="Directory & Masters", icon="book", group="Administration", status="soon",
         phase=2, admin_only=True, desc="Directory aur branch master update/search (sirf admin)."),
    dict(id="admin_users", name="Users & Access", icon="users", group="Administration", status="live",
         endpoint="admin.users", admin_only=True,
         desc="Signup approve karo, block/unblock, password reset aur har user ko tool access do."),
]

BY_ID = {m["id"]: m for m in MODULES}
ASSIGNABLE = [m for m in MODULES if not m.get("admin_only") and m["status"] != "external"]


def can_access(user, module_id: str) -> bool:
    m = BY_ID.get(module_id)
    if not user or not m:
        return False
    if user.get("role") == "admin":
        return True
    if m.get("admin_only"):
        return False
    if m["status"] == "external":
        return True
    mods = user.get("modules") or []
    return "*" in mods or module_id in mods


def grouped_for(user):
    """[(group, [modules...]), ...] containing only what this user may see."""
    out = []
    for g in GROUPS:
        items = [m for m in MODULES if m["group"] == g and can_access(user, m["id"])]
        if items:
            out.append((g, items))
    return out
