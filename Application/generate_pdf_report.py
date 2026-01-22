"""
PDF Report Generator for Hotel Booking Analysis
Creates a professional client-ready PDF report with graphs
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from datetime import datetime
import os

def create_pdf_report():
    """Generate professional PDF report"""
    
    # Create PDF
    pdf_filename = "Hotel_Booking_Analysis_Report.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.grey,
        spaceAfter=40,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    insight_style = ParagraphStyle(
        'Insight',
        parent=styles['BodyText'],
        fontSize=10,
        leftIndent=20,
        rightIndent=20,
        spaceBefore=10,
        spaceAfter=10,
        borderColor=colors.HexColor('#1f77b4'),
        borderWidth=1,
        borderPadding=10,
        backColor=colors.HexColor('#f0f2f6')
    )
    
    # Title Page
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph("Hotel Booking Analysis", title_style))
    elements.append(Paragraph("Data-Driven Insights for Business Optimization", subtitle_style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(f"Presented by: <b>Syed Muhammad Ali</b>", subtitle_style))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
    elements.append(PageBreak())
    
    # Executive Summary
    elements.append(Paragraph("Executive Summary", heading_style))
    elements.append(Paragraph(
        "This report analyzes <b>119,391 hotel booking records</b> from Resort and City Hotels to "
        "understand booking patterns, cancellation trends, and revenue opportunities. Our analysis reveals "
        "critical insights that can help improve booking retention and optimize pricing strategies.",
        body_style
    ))
    elements.append(Spacer(1, 0.3*inch))
    
    # Key Findings Overview
    elements.append(Paragraph("Key Findings at a Glance", heading_style))
    
    # Create summary table
    summary_data = [
        ['Metric', 'Value', 'Impact'],
        ['Overall Cancellation Rate', '37%', 'High Risk'],
        ['City Hotel Cancellations', '42%', 'Critical'],
        ['Resort Hotel Cancellations', '28%', 'Moderate'],
        ['Top Cancellation Country', 'Portugal (71%)', 'Concentrated Risk'],
        ['Primary Booking Channel', 'Online Agencies (47%)', 'High Volume'],
    ]
    
    summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(summary_table)
    elements.append(PageBreak())
    
    # Section 1: Cancellation Analysis
    elements.append(Paragraph("1. The Cancellation Challenge", heading_style))
    elements.append(Paragraph(
        "<b>The Problem:</b> Nearly 4 out of every 10 bookings (37%) are being canceled. "
        "This represents a significant revenue loss and creates operational challenges in planning and resource allocation.",
        body_style
    ))
    
    # Add graph 1
    if os.path.exists('report_images/1_cancellation_distribution.png'):
        img1 = Image('report_images/1_cancellation_distribution.png', width=5*inch, height=3.5*inch)
        elements.append(img1)
    
    elements.append(Paragraph(
        "<b>What This Means for Your Business:</b><br/>"
        "• Lost revenue from 37,000+ canceled bookings<br/>"
        "• Difficulty in accurate revenue forecasting<br/>"
        "• Wasted resources on bookings that don't materialize<br/>"
        "• Challenges in staff scheduling and planning",
        insight_style
    ))
    elements.append(PageBreak())
    
    # Section 2: Hotel Type Comparison
    elements.append(Paragraph("2. City vs Resort Hotels: A Tale of Two Properties", heading_style))
    elements.append(Paragraph(
        "<b>Key Discovery:</b> City Hotels face a 42% cancellation rate, while Resort Hotels have a more "
        "manageable 28% rate. This 14-percentage-point difference reveals that business travelers (who prefer "
        "city hotels) are less committed to their bookings than leisure travelers (who prefer resorts).",
        body_style
    ))
    
    if os.path.exists('report_images/2_hotel_comparison.png'):
        img2 = Image('report_images/2_hotel_comparison.png', width=5*inch, height=3.5*inch)
        elements.append(img2)
    
    elements.append(Paragraph(
        "<b>Strategic Implications:</b><br/>"
        "• City hotels need stricter cancellation policies<br/>"
        "• Focus retention efforts on business travelers<br/>"
        "• Resort hotels should maintain current strategies<br/>"
        "• One-size-fits-all approach won't work",
        insight_style
    ))
    elements.append(PageBreak())
    
    # Section 3: Pricing Analysis
    elements.append(Paragraph("3. Understanding Pricing Patterns", heading_style))
    elements.append(Paragraph(
        "<b>Pricing Intelligence:</b> Our analysis shows both hotel types maintain competitive pricing, "
        "with average daily rates ranging from $50-$150. City hotels show more price volatility due to "
        "fluctuating business travel demand, while resort hotels maintain steadier pricing patterns.",
        body_style
    ))
    
    if os.path.exists('report_images/3_adr_by_hotel.png'):
        img3 = Image('report_images/3_adr_by_hotel.png', width=6*inch, height=3*inch)
        elements.append(img3)
    
    elements.append(Paragraph(
        "<b>Revenue Opportunity:</b><br/>"
        "• Both properties are competitively priced<br/>"
        "• Seasonal pricing adjustments are working well<br/>"
        "• Focus should shift to retention rather than pricing changes<br/>"
        "• Dynamic pricing based on cancellation risk could be explored",
        insight_style
    ))
    elements.append(PageBreak())
    
    # Section 4: Seasonal Trends
    elements.append(Paragraph("4. Seasonal Booking Patterns", heading_style))
    elements.append(Paragraph(
        "<b>Seasonal Intelligence:</b> Summer months (June-August) show the highest booking volumes "
        "AND the highest cancellation volumes. This creates both opportunity and risk. The good news is "
        "that cancellations are predictable and follow booking patterns.",
        body_style
    ))
    
    if os.path.exists('report_images/4_monthly_cancellations.png'):
        img4 = Image('report_images/4_monthly_cancellations.png', width=5*inch, height=3.5*inch)
        elements.append(img4)
    
    elements.append(Paragraph(
        "<b>Action Plan:</b><br/>"
        "• Implement stronger retention efforts before summer season<br/>"
        "• Consider stricter cancellation policies during peak months<br/>"
        "• Offer early-bird discounts with commitment requirements<br/>"
        "• Use flexible policies in winter to maintain occupancy",
        insight_style
    ))
    elements.append(PageBreak())
    
    # Section 5: Geographic Analysis
    elements.append(Paragraph("5. The Portugal Problem: Geographic Insights", heading_style))
    elements.append(Paragraph(
        "<b>Critical Finding:</b> Portugal dominates cancellations with an overwhelming 71% of all "
        "canceled bookings. This concentration in a single market represents both a risk and an opportunity "
        "for targeted intervention.",
        body_style
    ))
    
    if os.path.exists('report_images/5_top_countries.png'):
        img5 = Image('report_images/5_top_countries.png', width=5*inch, height=4*inch)
        elements.append(img5)
    
    elements.append(Paragraph(
        "<b>Recommended Actions:</b><br/>"
        "• Investigate: Why are Portuguese guests canceling at such high rates?<br/>"
        "• Communicate: Improve Portuguese language support and customer service<br/>"
        "• Incentivize: Create targeted retention programs for Portuguese market<br/>"
        "• Partner: Work closely with Portuguese travel agencies to improve booking quality",
        insight_style
    ))
    elements.append(PageBreak())
    
    # Section 6: Price and Cancellation Relationship
    elements.append(Paragraph("6. The Price-Cancellation Connection", heading_style))
    elements.append(Paragraph(
        "<b>Interesting Pattern:</b> Our analysis reveals that canceled bookings tend to have slightly "
        "higher prices than completed bookings. This suggests price sensitivity plays a role in cancellation "
        "decisions. Higher-priced bookings may attract more cautious guests who are more likely to reconsider.",
        body_style
    ))
    
    if os.path.exists('report_images/6_adr_comparison.png'):
        img6 = Image('report_images/6_adr_comparison.png', width=5.5*inch, height=3.5*inch)
        elements.append(img6)
    
    elements.append(Paragraph(
        "<b>Strategic Response:</b><br/>"
        "• Consider tiered pricing with different cancellation terms<br/>"
        "• Offer incentives for non-refundable premium bookings<br/>"
        "• Create loyalty programs to offset price concerns<br/>"
        "• Provide price guarantees for committed bookings",
        insight_style
    ))
    elements.append(PageBreak())
    
    # Recommendations Section
    elements.append(Paragraph("Strategic Recommendations", heading_style))
    
    elements.append(Paragraph("<b>Immediate Actions (Next 30 Days):</b>", body_style))
    elements.append(Paragraph(
        "1. <b>Launch Portugal-Focused Retention Campaign</b><br/>"
        "   • Partner with Portuguese travel agencies<br/>"
        "   • Improve Portuguese language support<br/>"
        "   • Create special offers for Portuguese market<br/><br/>"
        "2. <b>Implement Tiered Cancellation Policies</b><br/>"
        "   • Offer discounts for non-refundable bookings<br/>"
        "   • Introduce flexible rebooking options<br/>"
        "   • Create premium packages with flexible terms<br/><br/>"
        "3. <b>Focus on City Hotel Retention</b><br/>"
        "   • Develop corporate loyalty programs<br/>"
        "   • Offer booking guarantees for business travelers<br/>"
        "   • Implement pre-arrival confirmation system",
        body_style
    ))
    
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("<b>Medium-Term Strategies (3-6 Months):</b>", body_style))
    elements.append(Paragraph(
        "4. <b>Optimize Online Booking Channels</b><br/>"
        "   • Work with OTAs to improve booking quality<br/>"
        "   • Incentivize direct bookings with exclusive perks<br/>"
        "   • Implement booking verification systems<br/><br/>"
        "5. <b>Dynamic Pricing Implementation</b><br/>"
        "   • Adjust prices based on cancellation risk profiles<br/>"
        "   • Offer seasonal promotions with commitment terms<br/>"
        "   • Test different pricing strategies by market segment<br/><br/>"
        "6. <b>Data-Driven Decision Making</b><br/>"
        "   • Implement real-time cancellation tracking dashboard<br/>"
        "   • Develop predictive models for cancellation risk<br/>"
        "   • Regular monthly analysis of booking patterns",
        body_style
    ))
    
    elements.append(PageBreak())
    
    # Expected Impact
    elements.append(Paragraph("Expected Business Impact", heading_style))
    
    impact_data = [
        ['Initiative', 'Expected Impact', 'Timeline'],
        ['Portugal-focused retention', '10-15% reduction in cancellations', '3 months'],
        ['Tiered cancellation policies', '5-8% increase in non-refundable bookings', '2 months'],
        ['City hotel improvements', '8-12% reduction in city cancellations', '4 months'],
        ['Channel optimization', '15-20% increase in direct bookings', '6 months'],
        ['Dynamic pricing', '5-10% revenue increase', '6 months'],
    ]
    
    impact_table = Table(impact_data, colWidths=[2.2*inch, 2.2*inch, 1.8*inch])
    impact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    elements.append(impact_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Conclusion
    elements.append(Paragraph("Conclusion", heading_style))
    elements.append(Paragraph(
        "The analysis reveals significant opportunities for revenue optimization through strategic cancellation "
        "reduction. By implementing targeted retention strategies, especially for the Portuguese market and city "
        "hotels, and optimizing booking channels, we can potentially recover millions in lost revenue annually.<br/><br/>"
        "The key to success lies in understanding that different guest segments require different approaches. "
        "Business travelers need flexibility and loyalty incentives, while leisure travelers respond to value "
        "propositions and early booking discounts.<br/><br/>"
        "With a data-driven approach and consistent execution of recommended strategies, we expect to see "
        "measurable improvements in cancellation rates within 3-6 months, leading to increased revenue stability "
        "and improved operational efficiency.",
        body_style
    ))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    elements.append(Paragraph("_" * 80, body_style))
    elements.append(Paragraph(
        "<b>Prepared by: Syed Muhammad Ali</b><br/>"
        "Data Analyst<br/>"
        f"Report Date: {datetime.now().strftime('%B %d, %Y')}<br/>"
        "Contact: Available for detailed analysis and implementation support",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
    ))
    
    # Build PDF
    doc.build(elements)
    print(f"✅ PDF Report Generated: {pdf_filename}")
    print(f"📄 Location: {os.path.abspath(pdf_filename)}")
    return pdf_filename

if __name__ == "__main__":
    print("🔄 Generating professional PDF report...")
    print("=" * 60)
    
    # Check if images exist
    required_images = [
        'report_images/1_cancellation_distribution.png',
        'report_images/2_hotel_comparison.png',
        'report_images/3_adr_by_hotel.png',
        'report_images/4_monthly_cancellations.png',
        'report_images/5_top_countries.png',
        'report_images/6_adr_comparison.png'
    ]
    
    missing_images = [img for img in required_images if not os.path.exists(img)]
    
    if missing_images:
        print("⚠️  Warning: Some images are missing:")
        for img in missing_images:
            print(f"   - {img}")
        print("\n💡 Run the export cell in your notebook first to generate all images.")
    else:
        print("✅ All graph images found!")
    
    print("\n🔄 Creating PDF...")
    try:
        pdf_file = create_pdf_report()
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Your professional PDF report is ready!")
        print("=" * 60)
        print(f"\n📁 File: {pdf_file}")
        print("\n📧 This report is ready to send to your client!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure reportlab is installed: pip install reportlab")
