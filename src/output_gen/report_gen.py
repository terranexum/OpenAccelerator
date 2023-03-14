import math
import os, sys
import pandas as pd
import locale
import datetime
import xlrd
import textwrap
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from os import devnull
from dotenv import load_dotenv

load_dotenv()

# Set the directory path to search
DIR_PATH = os.getenv('DIR_PATH')
width, height = letter


padding = dict(
  leftPadding=72, 
  rightPadding=72,
  topPadding=72,
  bottomPadding=18)

frame1 = Frame(0, 0, *letter, **padding)
frame2 = Frame(0, 0, *letter, **padding)
frame3 = Frame(0, 0, *letter, **padding)
frame4 = Frame(0, 0, *letter, **padding)
frame5 = Frame(0, 0, *letter, **padding)
frame6 = Frame(0, 0, *letter, **padding)
frame7 = Frame(0, 0, *letter, **padding)
frame8 = Frame(0, 0, *letter, **padding)




def generate_report_content(file_path, pdf_path, doc, can):

    # extract filename without extension
    filename = os.path.splitext(os.path.basename(pdf_path))[0]

    # remove last 4 characters
    asap_area = filename[:-4].strip()

    # get today's date for the new report date
    today = datetime.date.today()
    asap_date = today.strftime("%B %d, %Y")

    # read in data from utility spreadsheet
    wb = xlrd.open_workbook(file_path, logfile=open(devnull, 'w'))
    df = pd.read_excel(wb, engine='xlrd')

    total_cost = 0
    total_co2 = 0
    rshift = -2
    cshift = -1

    # Set the locale to the user's default
    locale.setlocale(locale.LC_ALL, '')

    # defining variables
    c_customer_base = 0
    c_annual_demand_kWh = 0
    c_annual_cost = 0
    c_co2_emissions = 0
    r_customer_base = 0
    r_annual_demand_kWh = 0
    r_annual_cost = 0
    r_co2_emissions = 0
    
    c_frac_cost_savings = 0.8
    r_frac_cost_savings = 0.8

    total_cost = 0
    total_co2 = 0

    current_mo = 0
    proposed_mo = 0
    c_pm_savings_mo = 0
    r_pm_savings_mo = 0
    savings_mo = 0
    savings_yr = 0

    pm_unit_gen_kWh = 0
    pm_unit_gen_capex = 0
    pm_unit_gen_count = 0
    pm_unit_storage_kWh = 0
    pm_unit_storage_capex = 0
    pm_unit_storage_count = 0
    pm_unit_shipping = 0
    pm_unit_w_profit = 0

    total_energy_usage = 0
    pm_system_capacity = 0
    pm_systems_needed = 0
    pm_system_cost = 0
    total_pm_systems_cost = 0
    pm_system_price = 0
    
    pm_system_savings_c_yr = 0
    pm_system_savings_r_yr = 0
    pm_system_savings = 0
    pm_total_savings = 0
    
    payback_period = 0

    # extract value of cells
    c_customer_base = df.iloc[40+rshift, 3+cshift]
    c_annual_demand_kWh = df.iloc[40+rshift, 4+cshift]
    c_annual_cost = df.iloc[40+rshift, 6+cshift]
    c_co2_emissions = df.iloc[40+rshift, 5+cshift]
    r_customer_base = df.iloc[41+rshift, 3+cshift]
    r_annual_demand_kWh = df.iloc[41+rshift, 4+cshift]
    r_annual_cost = df.iloc[41+rshift, 6+cshift]
    r_co2_emissions = df.iloc[41+rshift, 5+cshift] 

    no_elec_flag = False 
    payback_flag = False

    if not pd.isnull(c_customer_base): c_customer_base = pd.to_numeric(c_customer_base, errors='coerce', downcast='integer')
    else: c_customer_base = 0
        
    if not pd.isnull(c_annual_demand_kWh): c_annual_demand_kWh = pd.to_numeric(c_annual_demand_kWh, errors='coerce', downcast='integer')
    else: c_annual_demand_kWh = 0
    
    if not pd.isnull(c_annual_cost): c_annual_cost = c_annual_cost
    else: c_annual_cost = 0
    
    if not pd.isnull(c_co2_emissions): c_co2_emissions = pd.to_numeric(c_co2_emissions, errors='coerce', downcast='integer')
    else: c_co2_emissions = 0

    if not pd.isnull(r_customer_base): r_customer_base = pd.to_numeric(r_customer_base, errors='coerce', downcast='integer')
    else: r_customer_base = 0
        
    if not pd.isnull(r_annual_demand_kWh): r_annual_demand_kWh = pd.to_numeric(r_annual_demand_kWh, errors='coerce', downcast='integer')
    else: r_annual_demand_kWh = 0
    
    if not pd.isnull(r_annual_cost): r_annual_cost = r_annual_cost
    else: r_annual_cost = 0

    if not pd.isnull(r_co2_emissions): r_co2_emissions = pd.to_numeric(r_co2_emissions, errors='coerce', downcast='integer')
    else: r_co2_emissions = 0

    if c_customer_base == 0 or r_customer_base == 0:
        print("Customer count missing for", asap_area)
        no_elec_flag = True

    total_cost += c_annual_cost
    total_cost += r_annual_cost

    total_co2 += c_co2_emissions
    total_co2 += r_co2_emissions
    
    if no_elec_flag == False:
        # Define data for the table
        current_mo = locale.currency(c_annual_cost/c_customer_base/12, symbol=True, grouping=False)
        proposed_mo = locale.currency((c_annual_cost/c_customer_base/12)*(1-c_frac_cost_savings), symbol=True, grouping=False)
        c_pm_savings_mo = (c_annual_cost/c_customer_base/12)*(c_frac_cost_savings)
        savings_mo = locale.currency(c_pm_savings_mo, symbol=True, grouping=False)
        savings_yr = locale.currency(((c_annual_cost/c_customer_base/12)*(c_frac_cost_savings)) * 12, symbol=True, grouping=False)

        data_c = [
            ['Commercial Savings', 'Amount'],
            ['Monthly Electric Bill Today', str(current_mo)],
            ['Monthly Electric Bill after Prime Mover', str(proposed_mo)],
            ['Monthly Cost Savings', str(savings_mo)],
            ['Yearly Cost Savings', str(savings_yr)],
        ]

        current_mo = locale.currency(r_annual_cost/r_customer_base/12, symbol=True, grouping=False)
        proposed_mo = locale.currency((r_annual_cost/r_customer_base/12)*(1-r_frac_cost_savings), symbol=True, grouping=False)
        r_pm_savings_mo = (r_annual_cost/r_customer_base/12)*(r_frac_cost_savings)
        savings_mo = locale.currency(r_pm_savings_mo, symbol=True, grouping=False)
        savings_yr = locale.currency(((r_annual_cost/r_customer_base/12)*(r_frac_cost_savings)) * 12, symbol=True, grouping=False)

        data_r = [
            ['Residential Savings', 'Amount'],
            ['Monthly Electric Bill Today', str(current_mo)],
            ['Monthly Electric Bill after Prime Mover', str(proposed_mo)],
            ['Monthly Cost Savings', str(savings_mo)],
            ['Yearly Cost Savings', str(savings_yr)],
        ]

        pm_unit_gen_kWh = 20.484
        pm_unit_gen_capex = 27000
        pm_unit_gen_count = 0
        pm_unit_storage_kWh = 20
        pm_unit_storage_capex = 12882
        pm_unit_storage_count = 0
        pm_unit_shipping = 850
        pm_unit_w_profit = 1.20 * (pm_unit_gen_capex + pm_unit_storage_capex + pm_unit_shipping)

        # Calculate number of Prime Mover systems needed for 100% renewable energy
        total_energy_usage = r_annual_demand_kWh + c_annual_demand_kWh
        pm_system_capacity = pm_unit_storage_kWh
        pm_systems_needed = math.ceil(total_energy_usage / pm_system_capacity / 365)
        pm_system_cost = pm_unit_w_profit + pm_unit_shipping
        total_pm_systems_cost = locale.currency(pm_system_cost * pm_systems_needed, symbol=True, grouping=True)
        pm_system_price = locale.currency(pm_system_cost, symbol=True, grouping=True)
        
        pm_system_savings_c_yr = c_pm_savings_mo * 12
        pm_system_savings_r_yr = r_pm_savings_mo * 12
        pm_system_savings = pm_system_savings_c_yr + pm_system_savings_r_yr
        #print(total_cost, pm_system_savings)
        pm_total_savings = pm_system_savings * pm_systems_needed
        
        payback_period = (pm_system_cost * pm_systems_needed) / pm_total_savings
        if payback_period > 25:
            print("Payback period of", str(payback_period), "too long for", asap_area, ". Not outputting report.")
            payback_flag = True

        pm_systems_needed = locale.format_string("%d", pm_systems_needed, grouping=True)
        pm_system_savings = locale.currency(pm_system_savings, symbol=True, grouping=True)
        pm_total_savings = locale.currency(pm_total_savings, symbol=True, grouping=True)

    def wrap(c, s, f, h, w, x, y):
        c.setFont(f, h)
        linespacing = 5
        if len(s) > w:
            wrap_text = textwrap.wrap(s, width=w)
            for i in range(len(wrap_text)):
                yshift = (i * h) + linespacing
                
                c.drawString(x, y - yshift, wrap_text[i])
        else:
            c.drawString(x, y, s)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    PAGE 1
    Title page
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def page1(canvas, doc):

        canvas.saveState()

        #background
        canvas.drawImage("page1.jpg", 0, 0, width=width, height=height) 

        # content
        canvas.setFillColorRGB(255, 255, 255)

        canvas.setFont("Helvetica", 40)
        canvas.drawCentredString(width/2, 2.65 * inch, asap_area)

        canvas.setFont("Helvetica", 20)
        canvas.drawCentredString(width/2, 2 * inch, asap_date)

        canvas.setFont("Helvetica", 14)
        canvas.drawString(7.5 * inch, 0.5 * inch, str(canvas.getPageNumber()))

        '''
        #header
        canvas.drawString(0.5 * inch, 8 * inch, doc.fund.name)
        canvas.drawRightString(10.5 * inch, 8 * inch, doc.report_info)

        #footers
        canvas.drawString(0.5 * inch, 0.5 * inch, 'Larry Co.')
        canvas.drawRightString(10.5 * inch, 0.5 * inch, 'Page %d' % (doc.page))

        
        canvas.setStrokeGray(0.90)
        canvas.setFillGray(0.90)
        canvas.drawCentredString(5.5 * inch, 3.25 * inch, doc.watermark)
        '''
        canvas.restoreState()

        canvas.showPage()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    PAGE 2
    Introduction
        Brief overview of the purpose and goals of the plan
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def page2(canvas, doc):

        canvas.saveState()

        #background
        canvas.drawImage("page2.jpg", 0, 0, width=width, height=height) 

        # content
        canvas.setFillColorRGB(255, 255, 255)
        
        s = "TerraNexum's goal is to develop and help implement accelerated plans for renewable energy and energy storage deployment to achieve profitable emissions reduction at city and county levels - at the scale of multiple megatons of CO2 emissions reductions."
        wrap(canvas, s, "Helvetica", 16, 30, 0.75 * inch, 3.75 * inch)

        s = "Our ASAPs outline goals and strategies for achieving a complete shift to renewable energy on an accelerated timeline. At this time, we are presenting facts and figures for decarbonizing just electricity consumption through the use of new renewable energy production and energy storage systems."
        wrap(canvas, s, "Helvetica", 16, 30, 4.25 * inch, 3 * inch)

        canvas.setFont("Helvetica", 14)
        canvas.drawString(7.5 * inch, 0.5 * inch, str(canvas.getPageNumber()))

        canvas.restoreState()

        canvas.showPage()
        
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    PAGE 3
    Current Energy Usage and Cost

        Number of commercial customers and their total energy consumption in kWh last year
        Total cost of electricity for commercial customers
        Number of residential customers and their total energy consumption in kWh last year
        Total cost of electricity for residential customers

    The code adds a heading for the Current Energy Usage and Cost section to the 
    content list and creates a spacer to add some whitespace. It then creates a table 
    with the data and adds it to the content list.
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def page3(canvas, doc):

        canvas.saveState()

        #background
        canvas.drawImage("page3.jpg", 0, 0, width=width, height=height) 
        canvas.setFillColorRGB(0, 0, 0)
        
        if no_elec_flag == True:

            # content
            s = "Unfortunately, it seems there are no electrical customers here at the present."
            wrap(canvas, s, "Helvetica", 16, 35, 0.75 * inch, 7 * inch)

            s = "Although there are data for this locality for commercial and/or residential energy usage, no customers were reported receiving electric service. It is likely that the reported service is only for natural gas."
            wrap(canvas, s, "Helvetica", 16, 35, 0.75 * inch, 6 * inch)

            s = "Please check back at a later time when our ASAPs account for achieving emissions reductions where natural gas is being used as well."
            wrap(canvas, s, "Helvetica", 16, 35, 0.75 * inch, 4 * inch)

        else:

            # Create the table data
            c_customers = locale.format_string("%d", c_customer_base, grouping=True)
            r_customers = locale.format_string("%d", r_customer_base, grouping=True)

            c_kWh = locale.format_string("%d", c_annual_demand_kWh, grouping=True)
            r_kWh = locale.format_string("%d", r_annual_demand_kWh, grouping=True)

            c_cost = locale.currency(c_annual_cost, symbol=True, grouping=True)
            r_cost = locale.currency(r_annual_cost, symbol=True, grouping=True)

            c_co2 = locale.format_string("%d", c_co2_emissions, grouping=True)
            r_co2 = locale.format_string("%d", r_co2_emissions, grouping=True)

            data = [['', 'Commercial', 'Residential'],
                    ['Number of Customers', c_customers, r_customers],
                    ['Total kWh Consumed', c_kWh, r_kWh],
                    ['Total Cost of Electricity', c_cost, r_cost],
                    ['Total CO2 Emissions', c_co2, r_co2]
                    ]

            # content
            s = "The numbers below were supplied from the 2021 Community Energy Report for the " + asap_area + ", published by Xcel Energy and freely available on its website. A copy of this report is also available in our same GitHub repository folder where this ASAP was published."
            wrap(canvas, s, "Helvetica", 16, 35, 0.75 * inch, 7 * inch)

            s = "The potential is high for " + asap_area + " to achieve rapid emissions reductions."
            wrap(canvas, s, "Helvetica", 16, 35, 0.75 * inch, 5 * inch)

            # Create the table and add it to the content
            table = Table(data, style=[('GRID', (0, 0), (-1, -1), 1, colors.white),
                                    ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                                    ('FONTSIZE', (0, 1), (-1, -1), 12)])

            table.wrapOn(canvas, 6 * inch, 4 * inch) #width, height
            table.drawOn(canvas, 0.75 * inch, 2.5 * inch) #x, y

        canvas.setFont("Helvetica", 14)
        canvas.setFillColorRGB(255, 255, 255)
        canvas.drawString(7.5 * inch, 0.5 * inch, str(canvas.getPageNumber()))

        canvas.restoreState()

        canvas.showPage()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    PAGE 4
    Potential Cost Savings with Prime Mover System

        Cost of a Prime Mover system
        Potential revenue generation by owning a Prime Mover system
        Calculation of potential cost savings for commercial and residential customers who switch to Prime Mover systems

    This code creates a table with the relevant data, and adds a brief conclusion about
    the cost savings.
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def page4(canvas, doc):

        canvas.saveState()

        #background
        canvas.drawImage("page4.jpg", 0, 0, width=width, height=height) 

        # content
        canvas.setFillColorRGB(0, 0, 0)
        s =  "Our Prime Mover program offers a highly affordable means for commercial and industrial building owners to benefit from lower electric bills in the process of becoming more sustainable and energy resilient. Our system of the same name consists of least one solar canopy and a battery energy storage unit. Not only is greater sustainability and resilience the result, market growth also results, fueling the need for more electricians, EV charging stations, and more EVs in general."  
        wrap(canvas, s, "Helvetica", 15, 70, 0.75 * inch, 9.75 * inch)

        if no_elec_flag == False:

            # Add the table
            table = Table(data_c, style=[('GRID', (0, 0), (-1, -1), 1, colors.black),
                                    ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                                    ('FONTSIZE', (0, 1), (-1, -1), 10)])
            table.wrapOn(canvas, 6 * inch, 2 * inch) #width, height
            table.drawOn(canvas, 0.75 * inch, 5.25 * inch) #x, y

            # Add the table
            table = Table(data_r, style=[('GRID', (0, 0), (-1, -1), 1, colors.black),
                                ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('FONTSIZE', (0, 0), (-1, 0), 12),
                                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                                ('FONTSIZE', (0, 1), (-1, -1), 10)])
            table.wrapOn(canvas, 6 * inch, 2 * inch) #width, height
            table.drawOn(canvas, 4.25 * inch, 5.25 * inch) #x, y

        # content
        s = "This is made possible by Colorado's C-PACE, an innovative program that offers financing of up to 30 percent of a building's value, and assesses those repayments on the annual property tax for that property for up to 25 years. This financing is in addition to tax credits and incentives at federal, state, and local levels."
        wrap(canvas, s, "Helvetica", 15, 70, 0.75 * inch, 7.75 * inch)

        #s = "For residences, C-PACE is not available, but residential loans such as those available through Colorado's RENU program as well as federal and state tax credits already exist for home solar installations as well as battery storage."
        #wrap(canvas, s, "Helvetica", 12, 90, 0.75 * inch, 8.25 * inch)
        
        #s = "By purchasing one or more Prime Mover systems under our program, businesses can save significant amounts of money on their monthly electricity bills. Over the course of a year, this can add up to a substantial amount of savings, making the initial investment in the Prime Mover system well worth it."
        #wrap(canvas, s, "Helvetica", 12, 90, 0.75 * inch, 7.5 * inch)
        
        #s = "Prime Mover systems are ideal as the foundation of an open source hardware platform. Software that is developed by and for system users to expand the capabilities of their systems could be released for free under open source licenses for the broadest personal, non-profit, and commercial use."
        #wrap(canvas, s, "Helvetica", 12, 90, 0.75 * inch, 7.25 * inch)

        canvas.setFont("Helvetica", 14)
        canvas.drawString(7.5 * inch, 0.5 * inch, str(canvas.getPageNumber()))

        canvas.restoreState()

        canvas.showPage()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    PAGE 5
    Transition to 100% Renewable Energy
        Calculation of the number of Prime Mover systems needed to supply 100% renewable energy to commercial and residential customers
        Timeline for transition to 100% renewable energy

    This code calculates the number of Prime Mover systems needed to provide 100% 
    renewable energy for all residential and commercial customers, based on the total 
    energy usage calculated in the previous section. It then calculates the cost of 
    implementing the necessary number of systems, and notes that the revenue generated 
    by selling electricity back to the grid could help to pay for the systems in a 
    relatively short amount of time. Finally, it adds the content to the section and 
    appends it to the story.
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def page5(canvas, doc):

        canvas.saveState()

        #background
        canvas.drawImage("page5.jpg", 0, 0, width=width, height=height) 
        canvas.setFillColorRGB(255, 255, 255)

        pb_period = f'{payback_period: .2f}'
        
        if payback_flag == False and no_elec_flag == False:

            #s = "Prime Mover systems are ideal as the foundation of an open source hardware platform. Software that is developed by and for system users to expand the capabilities of their systems could be released for free under open source licenses for the broadest personal, non-profit, and commercial use."
            #wrap(canvas, s, "Helvetica", 14, 80, 0.75 * inch, 9.75 * inch)
            
            s = "A single Prime Mover system costs " + str(pm_system_price) + ". To transition to 100 percent renewable energy, it would require " + str(pm_systems_needed) + " Prime Mover systems to provide enough electricity for all residential and commercial customers in the " + asap_area + ". This would cost " + str(total_pm_systems_cost) + " to implement."
            wrap(canvas, s, "Helvetica", 14, 75, 0.75 * inch, 9.55 * inch)

            s = "With the energy savings Prime Mover owners would see by generating and storing their own electricity, which is " + str(pm_system_savings) + " per year per system and thus " + str(pm_total_savings) + " per year across all systems within the " + asap_area + ", the Prime Mover systems could pay for themselves in" + str(pb_period) + " years."
            wrap(canvas, s, "Helvetica", 14, 75, 0.75 * inch, 8.55 * inch)

            s = "This is, of course, too long for businesses to wait to be cash flow positive."
            wrap(canvas, s, "Helvetica", 14, 50, 3.25 * inch, 7.55 * inch)
        
            s = "For energy saving projects to be cash flow positive on day one with repayment periods of up to 25 years - it seems like this could change the game."
            wrap(canvas, s, "Helvetica", 16, 30, 4.5 * inch, 6.75 * inch)
        
            s = "It already has. Within Colorado alone, 118 such projects have been financed through C-PACE, resulting in 781,603 tons of lifetime GHG emissions reduction and $77.9M of lifetime cost savings. Projects have been as small as $53K to as large as $55.5M."
            wrap(canvas, s, "Helvetica", 16, 34, 0.75 * inch, 5 * inch)
        
        elif no_elec_flag == True:

            s = "Since the " + asap_area + " does not have electricity customers according to the records from the public utility, numbers cannot be reported right now because we do not yet have a system to help with natural gas emissions. We'll get there soon. In the meanwhile, it's worth knowing about what is available to finance energy efficiency projects for natural gas, such as boiler upgrades."
            wrap(canvas, s, "Helvetica", 16, 60, 0.75 * inch, 9.55 * inch)

            s = "For energy saving projects to be cash flow positive on day one with repayment periods of up to 25 years - it seems like this could change the game."
            wrap(canvas, s, "Helvetica", 16, 30, 4.5 * inch, 6.75 * inch)
        
            s = "It already has. Within Colorado alone, 118 such projects have been financed through C-PACE, resulting in 781,603 tons of lifetime GHG emissions reduction and $77.9M of lifetime cost savings. Projects have been as small as $53K to as large as $55.5M."
            wrap(canvas, s, "Helvetica", 16, 34, 0.75 * inch, 5 * inch)
        
        else:
            
            s = "A single Prime Mover system costs " + str(pm_system_price) + ". To transition to 100 percent renewable energy, the number of systems needed relative to the amount spent on electricity yields a payback period currently too long for the use of our Prime Mover systems alone. We will be working to improve our solutions for the " + asap_area + " in the near future."
            wrap(canvas, s, "Helvetica", 16, 60, 0.75 * inch, 9.55 * inch)

            s = "For energy saving projects to be cash flow positive on day one with repayment periods of up to 25 years - it seems like this could change the game."
            wrap(canvas, s, "Helvetica", 16, 30, 4.5 * inch, 6.75 * inch)
        
            s = "It already has. Within Colorado alone, 118 such projects have been financed through C-PACE, resulting in 781,603 tons of lifetime GHG emissions reduction and $77.9M of lifetime cost savings. Projects have been as small as $53K to as large as $55.5M."
            wrap(canvas, s, "Helvetica", 16, 34, 0.75 * inch, 5 * inch)
        

        canvas.setFont("Helvetica", 14)
        canvas.drawString(7.5 * inch, 0.5 * inch, str(canvas.getPageNumber()))

        canvas.restoreState()

        canvas.showPage()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    PAGE 6
    C-PACE - Making it Happen
        C-PACE Program Information 
        Timeline for transition to 100% renewable energy
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def page6(canvas, doc):

        canvas.saveState()

        #background
        canvas.drawImage("page6.jpg", 0, 0, width=width, height=height) 
        canvas.setFillColorRGB(0, 0, 0)

        # content
        s = "C-PACE (Colorado Property Assessed Clean Energy) is an innovative financing program for projects in renewable energy, energy efficiency, and water conservation, to include both retrofits as well as new construction. Projects are financed through private capital and the program was designed to be self-sustaining."
        wrap(canvas, s, "Helvetica", 12, 46, 0.75 * inch, 7.75 * inch)

        s = "The Rocky Mountain Institute (RMI) in February 2020 reported that financed projects offered a 15 percent or greater savings with bundled low and no cost improvements, a 35 percent savings with capital improvements, NOI (net operating income) increases between 2.4 and 5.6%, and property value increases between $5 and $11 per SF. Thus, for a 50,000 SF building, a building owner could see $250,000 to $550,000 in increased value."
        wrap(canvas, s, "Helvetica", 12, 46, 0.75 * inch, 6.25 * inch)

        s = "The benefits: 1) 100 percent financing - no out-of-pocket expenses, 2) is long-term, up to 25 years at a fixed interest rate, and 3) financing is done through a special purpose tax assessment on a property, such that C-PACE payments get paid annually through the property tax bill. The repayment obligation is transferrable to new building owners upon sale of the property, and no personal guarantees or positive cash flow are required to secure this financing. If you have tenants or hotel guests, the tax assessment can be passed through to them."
        wrap(canvas, s, "Helvetica", 12, 46, 0.75 * inch, 4.35 * inch)

        s = "The goal of C-PACE is for energy savings to be greater than the PACE payments, enabling cash flow positive projects from day one."
        wrap(canvas, s, "Helvetica", 12, 46, 0.75 * inch, 2 * inch)

        #s = "Eligible commercial and industrial property types include: offices, retail stores, hotels, industrial plants, agricultural facilities, healthcare facilities, mixed-use facilities, education (non-public), warehouses/storage buildings, non-profit buildings (non-public), and multifamily buildings with 5 or more units."
        #wrap(canvas, s, "Helvetica", 10, 56, 0.75 * inch, 4.25 * inch)

        #s = "Eligible improvements include solar PV, EV charging stations, energy storage, beneficial electrification, high-efficiency lighting, and more. Costs related to eligible improvements are also eligible, which include: engineering studies, architectural fees, energy audits, renewable energy feasibility studies, roof upgrades associated with rooftop solar PV, building structural reinforcement upgrades to support rooftop solar PV, environmental clean-up activities needed to install eligible equipment, commissioning and maintenance contracts up to five years, equipment extended warranties (as for PV system inverters), finance closing costs, and fees to administer the program (2.25 percent of project costs, capped at $50,000."
        #wrap(canvas, s, "Helvetica", 10, 56, 0.75 * inch, 3.5 * inch)       

        canvas.setFont("Helvetica", 14)
        canvas.setFillColorRGB(255, 255, 255)
        canvas.drawString(7.5 * inch, 0.5 * inch, str(canvas.getPageNumber()))

        canvas.restoreState()

        canvas.showPage()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    PAGE 7
    Community Benefits through TerraNexum
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def page7(canvas, doc):

        canvas.saveState()

        #background
        canvas.drawImage("page7.jpg", 0, 0, width=width, height=height) 

        # content
        canvas.setFillColorRGB(255, 255, 255)
        s = "Our name, TerraNexum, means 'earth network.' We work to accelerate the energy and carbon transition by designing intelligent networks of systems able to advance sustainability and resilience. We develop these systems through applying our extensive knowledge in managing energy, carbon, and other resources, and we design optimized networks to aid in energy, resource, and information flows using the tools of quantum optimization, geospatial and subsurface analytics, and cloud computing."
        wrap(canvas, s, "Helvetica", 12, 70, 1.5 * inch, 8.75 * inch)  

        s = "Our energy and carbon management partners are in all major stakeholder areas, from renewable energy production and storage to electric utilities, companies who wish to remove carbon from the atmosphere, even companies wishing to renovate old oil/gas reservoirs to provide clean, large-scale utility storage of renewable energy. Wherever energy and carbon intersect, there is a point on our network to integrate that work."
        wrap(canvas, s, "Helvetica", 12, 70, 1.5 * inch, 7.25 * inch)  

        s = "Our technology partners include businesses within cloud computing and quantum computing. We are participants within NVIDIA's Inception Program, Microsoft's Startups Hub, and AWS Activate."
        wrap(canvas, s, "Helvetica", 12, 70, 1.5 * inch, 5.85 * inch)  

        s = "Our community partners include universities and groups able to benefit from the free and open-source, open-hardware work we do and seek to continue to do. We are seeking to help local universities within Colorado raise $30M for both quantum and sustainability R&D and workforce development."
        wrap(canvas, s, "Helvetica", 12, 70, 1.5 * inch, 5.25 * inch)  

        s = "Our next step, with the data and results provided in this report, is to create a detailed geospatial visualization of how " + asap_area + " can be serviced over time to reach 100 percent enewable energy over various timeframes. Watch how the energy transition could unfold, through monthly snapshots into the future."
        wrap(canvas, s, "Helvetica", 12, 70, 1.5 * inch, 4.25 * inch)  

        s = "For additional information on any of the above and for references for your further outreach, please reach out."
        wrap(canvas, s, "Helvetica", 12, 70, 1.5 * inch, 3.25 * inch)  
        
        canvas.setFont("Helvetica", 14)
        canvas.drawString(7.5 * inch, 0.5 * inch, str(canvas.getPageNumber()))

        canvas.restoreState()

        canvas.showPage()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    PAGE 8
    Contact Information
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def page8(canvas, doc):

        canvas.saveState()

        #background
        canvas.drawImage("page8.jpg", 0, 0, width=width, height=height) 
        
        # content
        canvas.setFillColorRGB(255, 255, 255)
        s = "For Prime Mover Program inquiries, please contact Dahl Winters, CEO at TerraNexum, at dwinters@terranexum.com."
        wrap(canvas, s, "Helvetica", 12, 35, 0.95 * inch, 3.15 * inch) 
        
        s = "For C-PACE inquiries, please contact Tracy Phillips, the Program Director at C-PACE, at tphillips@copace.com, 720-933-8143."
        wrap(canvas, s, "Helvetica", 12, 40, 4.75 * inch, 3.15 * inch)  

        canvas.setFont("Helvetica", 14)
        canvas.drawString(7.5 * inch, 0.5 * inch, str(canvas.getPageNumber()))

        canvas.restoreState()

        canvas.showPage()


    # Create the templates for each page to be added
    page_templates = []
    page_template_1 = PageTemplate(id="page1", frames=frame1, onPage=page1(can, doc), pagesize=letter)
    page_template_2 = PageTemplate(id="page2", frames=frame2, onPage=page2(can, doc), pagesize=letter)
    page_template_3 = PageTemplate(id="page3", frames=frame3, onPage=page3(can, doc), pagesize=letter)
    page_template_4 = PageTemplate(id="page4", frames=frame4, onPage=page4(can, doc), pagesize=letter)
    page_template_5 = PageTemplate(id="page5", frames=frame5, onPage=page5(can, doc), pagesize=letter)
    page_template_6 = PageTemplate(id="page6", frames=frame6, onPage=page6(can, doc), pagesize=letter)
    page_template_7 = PageTemplate(id="page7", frames=frame7, onPage=page7(can, doc), pagesize=letter)
    page_template_8 = PageTemplate(id="page8", frames=frame8, onPage=page8(can, doc), pagesize=letter)
    page_templates.append(page_template_1)
    page_templates.append(page_template_2)
    page_templates.append(page_template_3)
    page_templates.append(page_template_4)
    page_templates.append(page_template_5)
    page_templates.append(page_template_6)
    page_templates.append(page_template_7)
    page_templates.append(page_template_8)
    doc.addPageTemplates(page_templates)

    #print('Working on', file_path)


    

    '''
    Introduction
        Brief overview of the purpose and goals of the plan

    Current Energy Usage and Cost
        Number of commercial customers and their total energy consumption in kWh last year
        Total cost of electricity for commercial customers
        Number of residential customers and their total energy consumption in kWh last year
        Total cost of electricity for residential customers

    Potential Cost Savings with Prime Mover System
        Cost of a Prime Mover system
        Potential revenue generation by owning a Prime Mover system
        Calculation of potential cost savings for commercial and residential customers who switch to Prime Mover systems

    Transition to 100% Renewable Energy
        Calculation of the number of Prime Mover systems needed to supply 100% renewable energy to commercial and residential customers
        Timeline for transition to 100% renewable energy

    Conclusion
        Summary of the plan and its potential benefits
    '''

    # Define styles
    #styles = getSampleStyleSheet()
    #styles.add(ParagraphStyle(name='Center', alignment=1))


    # Create a list for the individual content to be added
    #content = []
    #return content




print('dir_path', DIR_PATH)
# Loop through all files in the directory
for root, dirs, files in os.walk(DIR_PATH):
    for file in files:
        # Check if the file has a .xls extension
        if file.endswith('.xls'):

            try:
                # Get the full path to the file
                file_path = os.path.join(root, file)
                
                # Create a new PDF with reportlab
                pdf_path = os.path.splitext(file_path)[0] + '.pdf'

                if os.path.exists(pdf_path): os.remove(pdf_path) 

                # create a PDF document with letter size paper
                doc = BaseDocTemplate(pdf_path, pagesize=letter, rightMargin=72,
                    leftMargin=72, topMargin=72, bottomMargin=72)

                can = canvas.Canvas(pdf_path)

                # Add content to the PDF here and build
                generate_report_content(file_path, pdf_path, doc, can)

                #if len(report) > 0: #and len(page_templates) > 0:
                    #doc.addPageTemplates(page_templates)

                can.save()

                #doc.build(report) # canvasmaker=canvas.Canvas)

            except Exception as err:
                print(pdf_path, f"Unexpected {err=}, {type(err)=}")
                raise


            #sys.exit(1)
