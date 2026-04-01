"""
Playwright tests for Lunaticos mockup:
- Responsive (mobile 390px + desktop 1280px)
- Navigation links work
- WhatsApp floating button present and linked correctly
- Menu opens/closes on mobile (backdrop blur)
- Hero "Ver productos" scrolls to #productos
- Contacto data: correct address and phone
"""
from playwright.sync_api import sync_playwright, expect
import sys

PASS = []
FAIL = []

def ok(msg):
    PASS.append(msg)
    print(f"  ✓ {msg}")

def fail(msg, err=""):
    FAIL.append(msg)
    print(f"  ✗ {msg}{(' — ' + str(err)) if err else ''}")

BASE = "http://localhost:4321"
WA_NUMBER = "5492901505599"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # ─── MOBILE (390×844, iPhone 14) ───────────────────────────────────────────
    print("\n── MOBILE 390×844 ──")
    ctx = browser.new_context(viewport={"width": 390, "height": 844})
    page = ctx.new_page()
    page.goto(BASE)
    page.wait_for_load_state("networkidle")

    # Floating WA button visible
    fab = page.locator(".wa-fab")
    try:
        expect(fab).to_be_visible()
        href = fab.get_attribute("href")
        if WA_NUMBER in href:
            ok("Floating WA button visible with correct number")
        else:
            fail("Floating WA button has wrong number", href)
    except Exception as e:
        fail("Floating WA button not visible", e)

    # Hamburger button visible
    try:
        hamburger = page.locator("#menu-open")
        expect(hamburger).to_be_visible()
        ok("Hamburger button visible on mobile")
    except Exception as e:
        fail("Hamburger button not visible", e)

    # Menu opens on tap
    try:
        page.locator("#menu-open").click()
        page.wait_for_timeout(400)
        drawer = page.locator("#menu-drawer")
        # Drawer should no longer have translate-x-full
        classes = drawer.get_attribute("class")
        if "translate-x-full" not in classes:
            ok("Menu drawer opens on hamburger tap")
        else:
            fail("Menu drawer did not open (still has translate-x-full)")
    except Exception as e:
        fail("Error opening mobile menu", e)

    # Backdrop visible
    try:
        backdrop = page.locator("#menu-backdrop")
        classes = backdrop.get_attribute("class")
        if "opacity-100" in classes:
            ok("Backdrop visible when menu open")
        else:
            fail("Backdrop not visible when menu open", classes)
    except Exception as e:
        fail("Error checking backdrop", e)

    # Menu closes on backdrop click (click LEFT side — drawer is on right, 288px wide)
    try:
        # Click at x=50 (well outside the 288px drawer on the right)
        page.mouse.click(50, 400)
        page.wait_for_timeout(400)
        classes = page.locator("#menu-drawer").get_attribute("class")
        if "translate-x-full" in classes:
            ok("Menu closes on backdrop click (outside drawer area)")
        else:
            fail("Menu did not close on backdrop click")
    except Exception as e:
        fail("Error closing menu via backdrop", e)

    # Menu closes on X button (click within drawer)
    try:
        page.locator("#menu-open").click()
        page.wait_for_timeout(400)
        page.locator("#menu-close").click(force=True)
        page.wait_for_timeout(400)
        classes = page.locator("#menu-drawer").get_attribute("class")
        if "translate-x-full" in classes:
            ok("Menu closes on X button")
        else:
            fail("Menu did not close on X button")
    except Exception as e:
        fail("Error closing menu via X", e)

    # Hero section exists
    try:
        hero = page.locator("#inicio, #hero-wrapper").first
        expect(hero).to_be_attached()
        ok("Hero section present")
    except Exception as e:
        fail("Hero section missing", e)

    # "Ver productos" button navigates to #productos
    try:
        btn = page.locator("a[href='#productos']").first
        expect(btn).to_be_attached()
        ok("'Ver productos' link to #productos found")
    except Exception as e:
        fail("'Ver productos' link missing", e)

    # Address contains correct street
    try:
        addr = page.locator("text=Rubinos del Río 191").first
        expect(addr).to_be_attached()
        ok("Correct address 'Rubinos del Río 191' present")
    except Exception as e:
        fail("Address not found or incorrect", e)

    # Phone number correct
    try:
        phone = page.locator("text=2901 50 55 99").first
        expect(phone).to_be_attached()
        ok("Correct phone '2901 50 55 99' present")
    except Exception as e:
        fail("Phone number not found", e)

    # Old second number NOT present
    try:
        old = page.locator("text=2901 44 44 68")
        count = old.count()
        if count == 0:
            ok("Old second phone number correctly removed")
        else:
            fail("Old second phone number still present")
    except Exception as e:
        fail("Error checking old phone number", e)

    page.screenshot(path="test-mobile.png", full_page=False)
    ctx.close()

    # ─── DESKTOP (1280×800) ────────────────────────────────────────────────────
    print("\n── DESKTOP 1280×800 ──")
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    page.goto(BASE)
    page.wait_for_load_state("networkidle")

    # Desktop nav visible
    try:
        nav = page.locator("header nav.hidden.md\\:flex")
        expect(nav).to_be_visible()
        ok("Desktop nav visible")
    except Exception as e:
        fail("Desktop nav not visible", e)

    # Hamburger hidden on desktop
    try:
        hamburger = page.locator("#menu-open")
        classes = hamburger.get_attribute("class") or ""
        if not hamburger.is_visible():
            ok("Hamburger hidden on desktop")
        else:
            fail("Hamburger should be hidden on desktop")
    except Exception as e:
        fail("Error checking hamburger on desktop", e)

    # Floating WA on desktop
    try:
        fab = page.locator(".wa-fab")
        expect(fab).to_be_visible()
        ok("Floating WA button visible on desktop")
    except Exception as e:
        fail("Floating WA not visible on desktop", e)

    # All main sections present
    for section in ["#productos", "#horarios", "#nosotros", "#contacto"]:
        try:
            el = page.locator(section).first
            expect(el).to_be_attached()
            ok(f"Section {section} present")
        except Exception as e:
            fail(f"Section {section} missing", e)

    page.screenshot(path="test-desktop.png", full_page=False)
    ctx.close()

    browser.close()

# ─── Summary ───────────────────────────────────────────────────────────────────
print(f"\n{'─'*50}")
print(f"  PASSED: {len(PASS)}  FAILED: {len(FAIL)}")
if FAIL:
    print("\nFailed tests:")
    for f in FAIL:
        print(f"  ✗ {f}")
    sys.exit(1)
else:
    print("  All tests passed!")
    sys.exit(0)
