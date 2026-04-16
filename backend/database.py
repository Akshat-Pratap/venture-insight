"""
Database engine, session management, and seed data for Venture Insight.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, StartupHistorical

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./venture_insight.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables and seed historical data if empty."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        count = db.query(StartupHistorical).count()
        if count == 0:
            _seed_historical_data(db)
    finally:
        db.close()


def _seed_historical_data(db):
    """Insert 30 realistic historical startup records."""
    startups = [
        # ─── Success Stories ────────────────────────────────────
        StartupHistorical(
            name="Airbnb",
            industry="Travel & Hospitality",
            funding="$6.4B",
            outcome="success",
            founded_year=2008,
            description="Peer-to-peer marketplace for short-term lodging. Disrupted the hotel industry by enabling homeowners to rent spare rooms. IPO in 2020 at $47B valuation."
        ),
        StartupHistorical(
            name="Stripe",
            industry="FinTech",
            funding="$2.3B",
            outcome="success",
            founded_year=2010,
            description="Online payment processing platform for internet businesses. Simplified payment integration for developers. Valued at $95B at peak."
        ),
        StartupHistorical(
            name="Slack",
            industry="Enterprise SaaS",
            funding="$1.4B",
            outcome="success",
            founded_year=2013,
            description="Business communication platform that replaced email for teams. Acquired by Salesforce for $27.7B in 2021."
        ),
        StartupHistorical(
            name="Zoom",
            industry="Communication Technology",
            funding="$161M",
            outcome="success",
            founded_year=2011,
            description="Video conferencing platform that became essential during COVID-19. IPO in 2019, market cap exceeded $160B at peak."
        ),
        StartupHistorical(
            name="Canva",
            industry="Design Technology",
            funding="$572M",
            outcome="success",
            founded_year=2012,
            description="Online graphic design platform democratizing design for non-designers. Valued at $40B, profitable with 130M monthly users."
        ),
        StartupHistorical(
            name="Shopify",
            industry="E-Commerce",
            funding="$122M",
            outcome="success",
            founded_year=2006,
            description="E-commerce platform enabling anyone to set up an online store. IPO in 2015, powering millions of businesses worldwide."
        ),
        StartupHistorical(
            name="SpaceX",
            industry="Aerospace",
            funding="$9.5B",
            outcome="success",
            founded_year=2002,
            description="Aerospace manufacturer and space transport company. Developed reusable rockets, reducing launch costs by 10x. Valued at $180B+."
        ),
        StartupHistorical(
            name="Databricks",
            industry="Data & AI",
            funding="$4.1B",
            outcome="success",
            founded_year=2013,
            description="Unified analytics platform built on Apache Spark. Serves enterprise data engineering and ML workloads. Valued at $43B."
        ),
        StartupHistorical(
            name="Figma",
            industry="Design Technology",
            funding="$333M",
            outcome="success",
            founded_year=2012,
            description="Collaborative interface design tool in the browser. Adobe attempted $20B acquisition. Revolutionized design collaboration."
        ),
        StartupHistorical(
            name="Notion",
            industry="Productivity SaaS",
            funding="$343M",
            outcome="success",
            founded_year=2013,
            description="All-in-one workspace combining notes, docs, wikis, and project management. Valued at $10B with millions of users."
        ),
        StartupHistorical(
            name="DoorDash",
            industry="Food Delivery",
            funding="$2.5B",
            outcome="success",
            founded_year=2013,
            description="Food delivery logistics platform. Became #1 delivery service in US. IPO in 2020 at $72B valuation."
        ),
        StartupHistorical(
            name="Rivian",
            industry="Electric Vehicles",
            funding="$10.7B",
            outcome="success",
            founded_year=2009,
            description="Electric adventure vehicle manufacturer. Backed by Amazon and Ford. IPO in 2021 at $77B valuation."
        ),
        StartupHistorical(
            name="UiPath",
            industry="Robotic Process Automation",
            funding="$2B",
            outcome="success",
            founded_year=2005,
            description="Enterprise robotic process automation platform. IPO in 2021 at $35B. Automates repetitive business processes."
        ),
        StartupHistorical(
            name="Plaid",
            industry="FinTech",
            funding="$734M",
            outcome="success",
            founded_year=2013,
            description="Financial data connectivity platform linking apps to bank accounts. Powers Venmo, Robinhood, and thousands of fintech apps."
        ),
        StartupHistorical(
            name="Discord",
            industry="Communication Technology",
            funding="$995M",
            outcome="success",
            founded_year=2015,
            description="Voice, video, and text communication platform. Originally for gamers, expanded to 150M+ monthly active users across communities."
        ),
        # ─── Failure Cases ──────────────────────────────────────
        StartupHistorical(
            name="Theranos",
            industry="Health Technology",
            funding="$1.4B",
            outcome="failure",
            founded_year=2003,
            description="Blood testing startup that claimed revolutionary finger-prick technology. Dissolved after fraud charges. Founder convicted."
        ),
        StartupHistorical(
            name="WeWork",
            industry="Real Estate / Co-Working",
            funding="$22B",
            outcome="failure",
            founded_year=2010,
            description="Co-working space provider that overexpanded. Failed IPO in 2019, valuation crashed from $47B to $9B. Filed bankruptcy in 2023."
        ),
        StartupHistorical(
            name="Quibi",
            industry="Media & Entertainment",
            funding="$1.75B",
            outcome="failure",
            founded_year=2018,
            description="Short-form mobile video streaming platform. Shut down after 6 months. Failed to find product-market fit despite massive funding."
        ),
        StartupHistorical(
            name="Jawbone",
            industry="Consumer Electronics",
            funding="$930M",
            outcome="failure",
            founded_year=1999,
            description="Wearable fitness tracker and Bluetooth speaker company. Couldn't compete with Fitbit and Apple Watch. Liquidated in 2017."
        ),
        StartupHistorical(
            name="Solyndra",
            industry="Clean Energy",
            funding="$1.1B",
            outcome="failure",
            founded_year=2005,
            description="Solar panel manufacturer that bet on cylindrical panels. Couldn't compete with cheap Chinese flat panels. Filed bankruptcy in 2011."
        ),
        StartupHistorical(
            name="Pets.com",
            industry="E-Commerce",
            funding="$110M",
            outcome="failure",
            founded_year=1998,
            description="Online pet supply retailer of the dot-com era. Spent heavily on marketing but sold products below cost. Shut down in 2000."
        ),
        StartupHistorical(
            name="Juicero",
            industry="Consumer Hardware",
            funding="$120M",
            outcome="failure",
            founded_year=2013,
            description="$400 WiFi-connected juicer that squeezed proprietary juice packs. Discovered packs could be squeezed by hand. Shut down in 2017."
        ),
        StartupHistorical(
            name="Katerra",
            industry="Construction Technology",
            funding="$2B",
            outcome="failure",
            founded_year=2015,
            description="Construction technology startup aiming to revolutionize building. Over-expanded, mismanaged funds. Filed bankruptcy in 2021."
        ),
        StartupHistorical(
            name="Fast",
            industry="FinTech",
            funding="$124.5M",
            outcome="failure",
            founded_year=2019,
            description="One-click checkout startup. Burned through cash with minimal revenue ($600K/year on $10M+/year burn). Shut down in 2022."
        ),
        StartupHistorical(
            name="Olive AI",
            industry="Health Technology",
            funding="$902M",
            outcome="failure",
            founded_year=2012,
            description="Healthcare AI automation platform. Raised nearly $1B but couldn't deliver on promises. Sold off assets and shut down in 2023."
        ),
        StartupHistorical(
            name="Zume Pizza",
            industry="Food Technology",
            funding="$445M",
            outcome="failure",
            founded_year=2015,
            description="Robot-powered pizza delivery startup backed by SoftBank. Pivoted multiple times. Couldn't make robotic food prep economical."
        ),
        StartupHistorical(
            name="ScaleFactor",
            industry="FinTech",
            funding="$100M",
            outcome="failure",
            founded_year=2014,
            description="AI-powered bookkeeping startup. Despite claiming AI automation, relied heavily on human accountants. Shut down in 2020."
        ),
        StartupHistorical(
            name="Munchery",
            industry="Food Delivery",
            funding="$125M",
            outcome="failure",
            founded_year=2010,
            description="Prepared meal delivery service. Couldn't achieve unit economics in competitive food delivery market. Shut down in 2019."
        ),
        StartupHistorical(
            name="Essential Products",
            industry="Consumer Electronics",
            funding="$330M",
            outcome="failure",
            founded_year=2015,
            description="Android creator's smartphone startup. Essential Phone praised by reviewers but sold poorly (~150K units). Shut down in 2020."
        ),
        StartupHistorical(
            name="Mixpanel (near-failure pivot)",
            industry="Analytics SaaS",
            funding="$77M",
            outcome="failure",
            founded_year=2009,
            description="Product analytics platform that over-expanded and nearly ran out of money. Had to do massive layoffs and pivot strategy to survive."
        ),
    ]

    db.add_all(startups)
    db.commit()
