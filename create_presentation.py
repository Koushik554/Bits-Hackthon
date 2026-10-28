import os
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

# 16:9 Widescreen dimensions (Points: 960 x 540)
PAGE_WIDTH = 960
PAGE_HEIGHT = 540

# Color Palette
BG_DARK = HexColor("#090D16")
BG_CARD = HexColor("#111827")
BG_CARD_LIGHT = HexColor("#1F293D")
BORDER_CARD = HexColor("#2D3748")

PRIMARY_CYAN = HexColor("#06B6D4")
PRIMARY_BLUE = HexColor("#3B82F6")
ACCENT_EMERALD = HexColor("#10B981")
ACCENT_AMBER = HexColor("#F59E0B")
ACCENT_ROSE = HexColor("#F43F5E")
ACCENT_PURPLE = HexColor("#8B5CF6")

TEXT_PRIMARY = HexColor("#FFFFFF")
TEXT_MUTED = HexColor("#94A3B8")
TEXT_BODY = HexColor("#E2E8F0")

def draw_header(c, title, subtitle, slide_num, total_slides=8):
    # Top bar accent line
    c.setFillColor(PRIMARY_CYAN)
    c.rect(0, PAGE_HEIGHT - 4, PAGE_WIDTH, 4, fill=1, stroke=0)
    
    # Title
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(45, PAGE_HEIGHT - 48, title)
    
    # Subtitle / Category
    c.setFillColor(PRIMARY_CYAN)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(45, PAGE_HEIGHT - 24, subtitle.upper())
    
    # Slide Number & Watermark
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 9)
    c.drawRightString(PAGE_WIDTH - 45, PAGE_HEIGHT - 35, f"HackSphere 3.0  |  {slide_num} / {total_slides}")
    
    # Divider line
    c.setStrokeColor(HexColor("#1E293B"))
    c.setLineWidth(1)
    c.line(45, PAGE_HEIGHT - 60, PAGE_WIDTH - 45, PAGE_HEIGHT - 60)

def draw_footer(c):
    c.setStrokeColor(HexColor("#1E293B"))
    c.setLineWidth(1)
    c.line(45, 30, PAGE_WIDTH - 45, 30)
    
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(45, 18, "Zoho Catalyst AppSail  *  QuickML Engine  *  BITS Pilani HackSphere 3.0")
    c.drawRightString(PAGE_WIDTH - 45, 18, "Confidential - Final Submission")

def draw_card(c, x, y, w, h, bg=BG_CARD, border=BORDER_CARD, radius=6):
    c.setFillColor(bg)
    c.setStrokeColor(border)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)

def draw_badge(c, text, x, y, color=PRIMARY_CYAN, text_color=TEXT_PRIMARY):
    c.setFont("Helvetica-Bold", 8)
    text_w = c.stringWidth(text, "Helvetica-Bold", 8)
    w = text_w + 14
    h = 16
    c.setFillColor(color)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.drawString(x + 7, y + 4, text)
    return w

# ----------------- SLIDES -----------------

def slide_1_title(c):
    # Background gradient simulation
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    
    # Geometric decorative accents
    c.setFillColor(HexColor("#0D1A30"))
    c.circle(PAGE_WIDTH - 120, PAGE_HEIGHT - 80, 200, fill=1, stroke=0)
    c.setFillColor(HexColor("#0E2342"))
    c.circle(PAGE_WIDTH - 60, PAGE_HEIGHT - 40, 130, fill=1, stroke=0)
    
    # Tag badge
    draw_badge(c, "HACKSPHERE 3.0  *  OFFICIAL PROJECT SUBMISSION", 60, PAGE_HEIGHT - 120, PRIMARY_BLUE)
    
    # Main Headline
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(60, PAGE_HEIGHT - 170, "Smart Energy Microgrid")
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(PRIMARY_CYAN)
    c.drawString(60, PAGE_HEIGHT - 215, "& Demand Forecasting Engine")
    
    # Subtitle
    c.setFillColor(TEXT_BODY)
    c.setFont("Helvetica", 14)
    c.drawString(60, PAGE_HEIGHT - 255, "Autonomous 24-Hour Energy Dispatch, BESS Battery Storage Simulation,")
    c.drawString(60, PAGE_HEIGHT - 275, "and Fail-Safe ML Telemetry deployed on Zoho Catalyst AppSail.")
    
    # Stats Row
    draw_card(c, 60, 90, 240, 110, bg=BG_CARD_LIGHT)
    c.setFillColor(ACCENT_EMERALD)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(80, 160, "13.35 kW")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(80, 140, "MODEL ACCURACY (RMSE)")
    c.setFont("Helvetica", 8)
    c.drawString(80, 115, "Random Forest + QuickML Ensemble")
    
    draw_card(c, 320, 90, 240, 110, bg=BG_CARD_LIGHT)
    c.setFillColor(PRIMARY_CYAN)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(340, 160, "500 kWh")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(340, 140, "BESS BATTERY SIMULATION")
    c.setFont("Helvetica", 8)
    c.drawString(340, 115, "80% Base SoC  *  10-100% Safety Bounds")
    
    draw_card(c, 580, 90, 320, 110, bg=BG_CARD_LIGHT)
    c.setFillColor(ACCENT_PURPLE)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(600, 160, "Zoho Catalyst")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(600, 140, "FULL-STACK DEPLOYMENT")
    c.setFont("Helvetica", 8)
    c.drawString(600, 115, "AppSail Python 3.9 + Interactive Dashboard")
    
    # Footer metadata
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(60, 45, "Platform: Zoho Catalyst  |  Repository: github.com/Koushik554/Bits-Hackthon")
    c.drawRightString(PAGE_WIDTH - 60, 45, "Verified: test_eval.py SUCCESS")

def slide_2_problem(c):
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    draw_header(c, "The Microgrid Challenge & Problem Context", "Challenge Overview", 2)
    draw_footer(c)
    
    # Left Column: The Problem
    draw_card(c, 45, 70, 415, 390)
    draw_badge(c, "THE OPERATIONAL CRISIS", 65, 425, ACCENT_ROSE)
    
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(65, 395, "Grid Overload & Renewable Intermittency")
    
    points_prob = [
        ("Peak Demand Spikes:", "Sudden surges (>160 kW) destabilize local distribution transformers, leading to brownouts and steep utility penalty tariffs."),
        ("Renewable Mismatch:", "Solar irradiance peaks midday when baseline demand is low, while evening hours (18:00-22:00) create critical grid stress."),
        ("Blind Load Switching:", "Traditional microgrids switch reactively AFTER grid overload occurs, risking micro-grid tripping and battery degradation."),
        ("Third-Party API Outages:", "Commercial cloud ML prediction endpoints can suffer network timeouts or quota exhaustion, crippling autonomous grid logic.")
    ]
    
    y = 355
    for title, desc in points_prob:
        c.setFillColor(ACCENT_AMBER)
        c.circle(73, y + 4, 3, fill=1, stroke=0)
        c.setFillColor(TEXT_PRIMARY)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(85, y, title)
        c.setFillColor(TEXT_MUTED)
        c.setFont("Helvetica", 9.5)
        # Wrap desc across 2 lines
        words = desc.split()
        line1 = " ".join(words[:9])
        line2 = " ".join(words[9:])
        c.drawString(85, y - 14, line1)
        c.drawString(85, y - 27, line2)
        y -= 62
        
    # Right Column: The Solution
    draw_card(c, 500, 70, 415, 390)
    draw_badge(c, "OUR HACKSPHERE 3.0 SOLUTION", 520, 425, ACCENT_EMERALD)
    
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(520, 395, "Predictive Smart Grid Controller")
    
    points_sol = [
        ("24-Hour Predictive Horizon:", "Forecasts hourly kW consumption before loads occur, using weather telemetry (Temp, Humidity, Solar Irradiance)."),
        ("Autonomous Transition Controller:", "Seamlessly shifts between Renewable Storage Mode and Main Grid Mode, buffering peak loads with zero human intervention."),
        ("High-Availability Fail-Safe Architecture:", "Dual-tier inference combining Zoho QuickML API with an onboard Random Forest fallback, guaranteeing 100% operational uptime."),
        ("Dynamic BESS Simulation (500 kWh):", "Simulates realistic battery state-of-charge (SoC) with 10%-100% safety bounds, 30% peak absorption, and off-peak recharge.")
    ]
    
    y = 355
    for title, desc in points_sol:
        c.setFillColor(PRIMARY_CYAN)
        c.circle(528, y + 4, 3, fill=1, stroke=0)
        c.setFillColor(TEXT_PRIMARY)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(540, y, title)
        c.setFillColor(TEXT_MUTED)
        c.setFont("Helvetica", 9.5)
        words = desc.split()
        line1 = " ".join(words[:9])
        line2 = " ".join(words[9:])
        c.drawString(540, y - 14, line1)
        c.drawString(540, y - 27, line2)
        y -= 62

def slide_3_architecture(c):
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    draw_header(c, "End-to-End System Architecture", "System Design", 3)
    draw_footer(c)
    
    steps = [
        ("1. TELEMETRY INGESTION", "CSV Upload & Interactive Form", "Extracts timestamps, cleans missing values with median imputation, and engineers hour & dayofweek features.", PRIMARY_BLUE),
        ("2. FORECASTING ENGINE", "QuickML + High-Availability RF", "Primary: Zoho QuickML REST API.\nFallback: Local Random Forest Regressor (RMSE 13.35 kW) ensuring continuous 24h predictions.", PRIMARY_CYAN),
        ("3. DISPATCH CONTROLLER", "Autonomous Switching Logic", "Evaluates hourly demand (>160 kW) and evening peak window (18:00-22:00) to trigger Renewable Storage Mode.", ACCENT_EMERALD),
        ("4. BESS SIMULATION", "500 kWh Battery Storage", "Tracks hourly State-of-Charge (SoC), discharging 30% of load during peak and charging at 40 kWh/h during off-peak.", ACCENT_AMBER),
        ("5. CATALYST APPSAIL", "Interactive Web Dashboard", "Alpine.js + Chart.js dashboard deployed on Catalyst with Overview, Grid Modes, Battery SoC, and Logs.", ACCENT_PURPLE),
    ]
    
    card_w = 160
    card_h = 340
    gap = 18
    start_x = 45
    y = 90
    
    for i, (title, sub, desc, color) in enumerate(steps):
        x = start_x + i * (card_w + gap)
        draw_card(c, x, y, card_w, card_h, bg=BG_CARD)
        
        # Color accent stripe
        c.setFillColor(color)
        c.rect(x, y + card_h - 4, card_w, 4, fill=1, stroke=0)
        
        # Step Tag
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x + 12, y + card_h - 22, title)
        
        # Subtitle
        c.setFillColor(TEXT_PRIMARY)
        c.setFont("Helvetica-Bold", 10.5)
        words = sub.split()
        if len(words) > 2:
            c.drawString(x + 12, y + card_h - 45, " ".join(words[:2]))
            c.drawString(x + 12, y + card_h - 58, " ".join(words[2:]))
        else:
            c.drawString(x + 12, y + card_h - 45, sub)
            
        c.setStrokeColor(HexColor("#263248"))
        c.line(x + 12, y + card_h - 70, x + card_w - 12, y + card_h - 70)
        
        # Description
        c.setFillColor(TEXT_MUTED)
        c.setFont("Helvetica", 8.5)
        lines = desc.split("\n")
        cur_y = y + card_h - 88
        for block in lines:
            words = block.split()
            buf = ""
            for w in words:
                if len(buf + " " + w) < 22:
                    buf += " " + w
                else:
                    c.drawString(x + 12, cur_y, buf.strip())
                    cur_y -= 13
                    buf = w
            if buf:
                c.drawString(x + 12, cur_y, buf.strip())
                cur_y -= 18

def slide_4_ml_engine(c):
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    draw_header(c, "ML Demand Forecasting & Fail-Safe Architecture", "Machine Learning Pipeline", 4)
    draw_footer(c)
    
    # Left Card: ML Features & Training
    draw_card(c, 45, 70, 415, 390)
    draw_badge(c, "FEATURE ENGINEERING & MODELING", 65, 425, PRIMARY_CYAN)
    
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(65, 395, "Telemetry Feature Extraction Pipeline")
    
    features = [
        ("hour (0-23)", "Captures distinct diurnal load cycles (daytime activity vs night)"),
        ("dayofweek (0-6)", "Distinguishes industrial/commercial weekdays from weekend baselines"),
        ("ambient_temp_c", "Primary thermal cooling load driver (air conditioning surge)"),
        ("humidity_pct", "Latent heat factor influencing HVAC electrical draw"),
        ("solar_irradiance_wm2", "Direct proxy for behind-the-meter solar offset capacity")
    ]
    
    y = 355
    for feat, purpose in features:
        draw_badge(c, feat, 65, y, HexColor("#1E3A5F"), PRIMARY_CYAN)
        c.setFillColor(TEXT_BODY)
        c.setFont("Helvetica", 9)
        c.drawString(65, y - 14, purpose)
        y -= 44
        
    c.setStrokeColor(HexColor("#263248"))
    c.line(65, 135, 440, 135)
    c.setFillColor(ACCENT_EMERALD)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(65, 115, "Model Architecture: Random Forest Ensemble")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(65, 95, "Trained on 4,000 historical rows with 300 estimators, min_samples_leaf=3.")
    c.drawString(65, 80, "Achieved Holdout RMSE: 13.35 kW (QuickML Benchmark: ~12.0 kW).")

    # Right Card: Resilience & Zero Downtime
    draw_card(c, 500, 70, 415, 390)
    draw_badge(c, "HIGH AVAILABILITY & QUOTA RESILIENCE", 520, 425, ACCENT_AMBER)
    
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(520, 395, "Zero-Downtime Prediction Architecture")
    
    resilience_items = [
        ("Zoho QuickML Quota Exhaustion:", "Free-tier limits (500 calls) trigger HTTP 403 PREDICTION_USAGE_LIMIT_EXCEEDED during bulk or repeated evaluations."),
        ("The 'Probe-First' Pattern:", "predict.py sends 1 single probe request to check QuickML availability. If accessible, it processes remaining rows via ThreadPoolExecutor."),
        ("Instant Autonomous Fallback:", "If QuickML returns 403, network failure, or timeout, the engine instantaneously switches to the local RF model without dropping a single row."),
        ("Self-Healing Retraining:", "If pre-pickled model_local.joblib is ever missing, predict.py auto-retrains from train_prepared.csv in <2 seconds."),
        ("Pre-Submission Verification:", "Evaluated against 1,000 test rows via test_eval.py with 100% SUCCESS.")
    ]
    
    y = 355
    for title, desc in resilience_items:
        c.setFillColor(ACCENT_AMBER)
        c.circle(528, y + 4, 3, fill=1, stroke=0)
        c.setFillColor(TEXT_PRIMARY)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(540, y, title)
        c.setFillColor(TEXT_MUTED)
        c.setFont("Helvetica", 8.5)
        words = desc.split()
        line1 = " ".join(words[:10])
        line2 = " ".join(words[10:])
        c.drawString(540, y - 13, line1)
        c.drawString(540, y - 24, line2)
        y -= 52

def slide_5_switching(c):
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    draw_header(c, "Transition Controller & Dispatch Logic", "Grid Automation Rules", 5)
    draw_footer(c)
    
    # 3 Rule Cards
    card_w = 270
    card_h = 380
    
    # Card 1: Renewable Storage Mode
    draw_card(c, 45, 75, card_w, card_h, bg=BG_CARD)
    c.setFillColor(ACCENT_EMERALD)
    c.rect(45, 75 + card_h - 4, card_w, 4, fill=1, stroke=0)
    draw_badge(c, "CONDITION A", 65, 420, ACCENT_EMERALD)
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(65, 390, "Renewable Storage Mode")
    
    c.setFillColor(PRIMARY_CYAN)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(65, 355, "Trigger Criteria:")
    c.setFillColor(TEXT_BODY)
    c.setFont("Helvetica", 10)
    c.drawString(65, 335, "* Demand > 160 kW")
    c.drawString(65, 315, "* OR Hour in [18:00, 22:00] (Inclusive)")
    
    c.setStrokeColor(HexColor("#263248"))
    c.line(65, 290, 290, 290)
    
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(65, 265, "Microgrid Dispatch Action:")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 9)
    actions_a = [
        "Switches power source from Main Grid",
        "to localized BESS battery storage.",
        "Discharges 30% of hourly load (kW)",
        "directly from the 500 kWh battery.",
        "Reduces peak utility power draw,",
        "lowering stress on substation lines."
    ]
    cur_y = 245
    for a in actions_a:
        c.drawString(65, cur_y, a)
        cur_y -= 16

    # Card 2: Main Grid Mode
    draw_card(c, 345, 75, card_w, card_h, bg=BG_CARD)
    c.setFillColor(PRIMARY_BLUE)
    c.rect(345, 75 + card_h - 4, card_w, 4, fill=1, stroke=0)
    draw_badge(c, "CONDITION B", 365, 420, PRIMARY_BLUE)
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(365, 390, "Main Grid Mode")
    
    c.setFillColor(PRIMARY_CYAN)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(365, 355, "Trigger Criteria:")
    c.setFillColor(TEXT_BODY)
    c.setFont("Helvetica", 10)
    c.drawString(365, 335, "* Demand <= 160 kW")
    c.drawString(365, 315, "* AND Hour outside 18:00-22:00")
    
    c.setStrokeColor(HexColor("#263248"))
    c.line(365, 290, 590, 290)
    
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(365, 265, "Microgrid Dispatch Action:")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 9)
    actions_b = [
        "Microgrid draws baseline load",
        "directly from primary utility grid.",
        "Activates off-peak BESS recharging",
        "at steady rate of 40 kWh / hour.",
        "Replenishes SoC by +8.0% / hour",
        "capped at 100% capacity limit."
    ]
    cur_y = 245
    for b in actions_b:
        c.drawString(365, cur_y, b)
        cur_y -= 16

    # Card 3: Critical Overload Alert
    draw_card(c, 645, 75, card_w, card_h, bg=BG_CARD)
    c.setFillColor(ACCENT_ROSE)
    c.rect(645, 75 + card_h - 4, card_w, 4, fill=1, stroke=0)
    draw_badge(c, "SAFETY OVERRIDE", 665, 420, ACCENT_ROSE)
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(665, 390, "Critical Overload Alert")
    
    c.setFillColor(ACCENT_AMBER)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(665, 355, "Trigger Criteria:")
    c.setFillColor(TEXT_BODY)
    c.setFont("Helvetica", 10)
    c.drawString(665, 335, "* Predicted Demand >= 200 kW")
    c.drawString(665, 315, "* Triggered INDEPENDENTLY of Mode")
    
    c.setStrokeColor(HexColor("#263248"))
    c.line(665, 290, 890, 290)
    
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(665, 265, "Emergency Protocol:")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 9)
    actions_c = [
        "Flashes high-priority UI alert banner.",
        "Emits instant log tag in telemetry.",
        "Pre-arms secondary load-shedding relays.",
        "Forces BESS maximum discharge rate.",
        "Protects transformer health and prevents",
        "cascading blackout shutdown."
    ]
    cur_y = 245
    for cc in actions_c:
        c.drawString(665, cur_y, cc)
        cur_y -= 16

def slide_6_bess(c):
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    draw_header(c, "Battery Energy Storage System (BESS) Simulation", "Energy Storage Dynamics", 6)
    draw_footer(c)
    
    # Left Card: Specifications & Math
    draw_card(c, 45, 70, 430, 390)
    draw_badge(c, "BESS MODEL SPECIFICATIONS", 65, 425, ACCENT_EMERALD)
    
    specs = [
        ("Total Battery Capacity:", "500 kWh (High-Density Lithium Iron Phosphate)"),
        ("Initial State of Charge:", "80.0% (400 kWh reserve at simulation start)"),
        ("Operational SoC Boundaries:", "10.0% Minimum (Floor) to 100.0% Maximum (Ceiling)"),
        ("SoC Safety Buffer:", "Protects cells against deep discharge damage (<10%)")
    ]
    y = 385
    for title, val in specs:
        c.setFillColor(TEXT_PRIMARY)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(65, y, title)
        c.setFillColor(PRIMARY_CYAN)
        c.setFont("Helvetica", 9.5)
        c.drawString(65, y - 14, val)
        y -= 38
        
    c.setStrokeColor(HexColor("#263248"))
    c.line(65, 230, 450, 230)
    
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(65, 210, "Mathematical Simulation Formulary")
    
    c.setFillColor(ACCENT_AMBER)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(65, 185, "Discharge Rate (Renewable Storage Mode):")
    c.setFillColor(TEXT_BODY)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(65, 170, "Delta SoC = - [ (0.30 x Demand_kW) / 500 kWh ] x 100%")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(65, 155, "Example: 180 kW demand discharges 54 kWh (-10.8% SoC/hr).")
    
    c.setFillColor(ACCENT_EMERALD)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(65, 130, "Recharge Rate (Main Grid Mode):")
    c.setFillColor(TEXT_BODY)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(65, 115, "Delta SoC = + [ 40 kWh / 500 kWh ] x 100% = + 8.0% / hr")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(65, 100, "Replenishes battery up to maximum 100.0% limit.")

    # Right Card: 24-Hour Simulation Trajectory
    draw_card(c, 500, 70, 415, 390)
    draw_badge(c, "SIMULATED 24-HOUR BESS PROFILE", 520, 425, PRIMARY_CYAN)
    
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(520, 395, "State of Charge (SoC) Dynamics")
    
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(520, 375, "Representative 24-Hour Cycle from sample_test_input.csv:")
    
    # Table of hours
    headers = ["Hour", "Demand", "Active Mode", "SoC Change", "Net SoC"]
    col_x = [520, 565, 630, 760, 845]
    
    c.setFillColor(HexColor("#1A2639"))
    c.rect(515, 345, 385, 20, fill=1, stroke=0)
    c.setFillColor(TEXT_PRIMARY)
    c.setFont("Helvetica-Bold", 8.5)
    for i, h in enumerate(headers):
        c.drawString(col_x[i], 351, h)
        
    sample_rows = [
        ("00:00", "125 kW", "Main Grid", "+8.0% (Charge)", "88.0%"),
        ("04:00", "110 kW", "Main Grid", "+8.0% (Charge)", "100.0% (Max)"),
        ("12:00", "175 kW", "Renewable Storage", "-10.5% (Discharge)", "89.5%"),
        ("15:00", "190 kW", "Renewable Storage", "-11.4% (Discharge)", "78.1%"),
        ("19:00", "215 kW", "Renewable + Alert", "-12.9% (Discharge)", "52.3%"),
        ("21:00", "195 kW", "Renewable Storage", "-11.7% (Discharge)", "28.9%"),
        ("23:00", "130 kW", "Main Grid", "+8.0% (Charge)", "36.9%")
    ]
    
    row_y = 325
    for r in sample_rows:
        if "Alert" in r[2]:
            c.setFillColor(HexColor("#3F151E"))
            c.rect(515, row_y - 4, 385, 18, fill=1, stroke=0)
            c.setFillColor(ACCENT_ROSE)
        else:
            c.setFillColor(TEXT_BODY)
        c.setFont("Helvetica", 8)
        c.drawString(col_x[0], row_y, r[0])
        c.drawString(col_x[1], row_y, r[1])
        c.drawString(col_x[2], row_y, r[2])
        c.drawString(col_x[3], row_y, r[3])
        c.drawString(col_x[4], row_y, r[4])
        row_y -= 22
        
    c.setFillColor(ACCENT_EMERALD)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(520, 100, "* Guaranteed Continuous Operation:")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(520, 85, "Battery remains within safe 10-100% operational bounds throughout 24-hour cycle.")

def slide_7_ui(c):
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    draw_header(c, "Zoho Catalyst AppSail Dashboard & UI", "Frontend Experience", 7)
    draw_footer(c)
    
    # 4 View Cards
    views = [
        ("VIEW 1: SYSTEM OVERVIEW", "Dual-Axis Forecasting Chart", [
            "* Real-time KPI Metric Cards (Active Load, Grid Status, Alert Counter).",
            "* Dual-Axis Forecast Chart: Predicted Demand (kW) vs. BESS Battery SoC (%).",
            "* Instant 24h, 48h, 7d Forecast Horizon Toggle.",
            "* Glassmorphism styling with dark mode and zero UI latency."
        ], PRIMARY_BLUE),
        ("VIEW 2: DISPATCH CONTROLLER", "Smart Grid Switching Analytics", [
            "* Visual breakdown of Renewable Storage Mode vs. Main Grid Mode hours.",
            "* Threshold indicator cards highlighting >160 kW and 18-22h evening peak.",
            "* Transition frequency monitor and peak-shaving summary.",
            "* Operational status chips with dynamic CSS pulsing badges."
        ], ACCENT_EMERALD),
        ("VIEW 3: BESS BATTERY MONITOR", "500 kWh State-of-Charge Dynamics", [
            "* High-precision battery gauge showing real-time SoC percentage.",
            "* Hourly discharge and charge trajectory timeline.",
            "* Safety threshold alerts for low-battery (<15%) and full reserve (100%).",
            "* Simulated energy savings calculation vs. standard utility tariff."
        ], ACCENT_AMBER),
        ("VIEW 4: REAL-TIME TELEMETRY LOG", "Filterable Table & CSV Export", [
            "* Complete tabular display of every forecast hour.",
            "* Search by timestamp and filter by Grid Mode or Overload status.",
            "* Ingest custom CSV telemetry or edit individual hour values.",
            "* One-click CSV export of predictions and control signals."
        ], ACCENT_PURPLE)
    ]
    
    grid_w = 425
    grid_h = 185
    positions = [(45, 275), (490, 275), (45, 75), (490, 75)]
    
    for i, (title, sub, bullets, color) in enumerate(views):
        x, y = positions[i]
        draw_card(c, x, y, grid_w, grid_h, bg=BG_CARD)
        c.setFillColor(color)
        c.rect(x, y + grid_h - 3, grid_w, 3, fill=1, stroke=0)
        
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(x + 15, y + grid_h - 18, title)
        
        c.setFillColor(TEXT_PRIMARY)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 15, y + grid_h - 36, sub)
        
        c.setFillColor(TEXT_MUTED)
        c.setFont("Helvetica", 8.5)
        by = y + grid_h - 55
        for b in bullets:
            c.drawString(x + 15, by, b)
            by -= 16

def slide_8_impact(c):
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    draw_header(c, "Impact, Evaluation Results & Future Scope", "Results & Conclusion", 8)
    draw_footer(c)
    
    # Left Card: Achievements & Results
    draw_card(c, 45, 70, 420, 390)
    draw_badge(c, "HACKATHON DELIVERABLES & RESULTS", 65, 425, ACCENT_EMERALD)
    
    results = [
        ("Evaluation Scorecard:", "Passed test_eval.py with 100% SUCCESS across 1,000 hidden test rows."),
        ("Forecasting Accuracy:", "Holdout RMSE of 13.35 kW on 800-row holdout set, achieving competitive parity with QuickML AutoML (~12.0 kW)."),
        ("Cloud Deployment:", "Fully hosted and live on Zoho Catalyst AppSail with zero configuration required by end users."),
        ("Security Compliance:", "Zero credentials in source control; .gitignore safeguards secrets and local model binaries."),
        ("Peak Load Reduction:", "30% peak demand shaving successfully reduces distribution transformer strain during 18:00-22:00 peak hours.")
    ]
    
    y = 390
    for title, desc in results:
        c.setFillColor(ACCENT_EMERALD)
        c.circle(73, y + 4, 3, fill=1, stroke=0)
        c.setFillColor(TEXT_PRIMARY)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(85, y, title)
        c.setFillColor(TEXT_MUTED)
        c.setFont("Helvetica", 8.5)
        words = desc.split()
        line1 = " ".join(words[:10])
        line2 = " ".join(words[10:])
        c.drawString(85, y - 13, line1)
        c.drawString(85, y - 24, line2)
        y -= 52
        
    c.setStrokeColor(HexColor("#263248"))
    c.line(65, 120, 440, 120)
    c.setFillColor(PRIMARY_CYAN)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(65, 100, "Repository: https://github.com/Koushik554/Bits-Hackthon")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(65, 85, "Live Web App: Zoho Catalyst AppSail (Microgrid Service)")

    # Right Card: Future Innovations
    draw_card(c, 495, 70, 420, 390)
    draw_badge(c, "FUTURE HORIZONS & ROADMAP", 515, 425, PRIMARY_BLUE)
    
    future = [
        ("Multi-Battery BESS Swarm Coordination:", "Scale from a single 500 kWh pack to a distributed network of commercial and residential batteries across the microgrid feeder."),
        ("Real-Time IoT Smart Meter Integration:", "Direct MQTT telemetry streaming via Zoho Catalyst IoT connectors for sub-minute dispatch adjustments."),
        ("Dynamic Real-Time Electricity Tariffs:", "Incorporate spot market power pricing to maximize battery charge during negative/cheap tariff windows and discharge during high-rate surges."),
        ("Automated Demand Response:", "Issue automated load-shedding commands to smart industrial appliances during Critical Overload Alerts (>=200 kW).")
    ]
    
    y = 390
    for title, desc in future:
        c.setFillColor(PRIMARY_CYAN)
        c.circle(523, y + 4, 3, fill=1, stroke=0)
        c.setFillColor(TEXT_PRIMARY)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(535, y, title)
        c.setFillColor(TEXT_MUTED)
        c.setFont("Helvetica", 8.5)
        words = desc.split()
        line1 = " ".join(words[:10])
        line2 = " ".join(words[10:])
        c.drawString(535, y - 13, line1)
        c.drawString(535, y - 24, line2)
        y -= 52
        
    c.setStrokeColor(HexColor("#263248"))
    c.line(515, 120, 890, 120)
    c.setFillColor(ACCENT_AMBER)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(515, 100, "Thank You, HackSphere 3.0 Organizers & BITS Pilani!")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(515, 85, "Ready for Q&A and Live Demo Evaluation.")

# ----------------- MAIN BUILD -----------------

def build_pdf(filename="HackSphere_3.0_Presentation.pdf"):
    c = canvas.Canvas(filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    slides = [
        slide_1_title,
        slide_2_problem,
        slide_3_architecture,
        slide_4_ml_engine,
        slide_5_switching,
        slide_6_bess,
        slide_7_ui,
        slide_8_impact
    ]
    
    for i, slide_fn in enumerate(slides):
        slide_fn(c)
        c.showPage()
        
    c.save()
    print(f"Successfully generated {filename} with {len(slides)} slides.")

if __name__ == "__main__":
    build_pdf()
