from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from matplotlib import pylab
from pylab import *
import PIL, PIL.Image
from io import BytesIO
import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as mlt
import seaborn as sns
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls
from subprocess import check_output
from django.conf import settings
import os
import bs4
import requests
import sweetify

mlt.style.use('fivethirtyeight')

def getStats(batsman, bowler):

    res = {}
    values = []

    url = "http://www.cricmetric.com/matchup.py?batsman="
    batsman.replace(' ', '+')
    bowler.replace(' ', '+')
    url += batsman + "&bowler=" + bowler

    response = requests.get(url) #"http://www.cricmetric.com/matchup.py?batsman=V+Kohli&bowler=MA+Starc"
    html = response.text
    # print(html)
    data = []


    # converting the html string to soup object
    soup = bs4.BeautifulSoup(html, "html.parser")
    ip = soup.select('.panel')

    for curr in ip:
        inner = curr.select('.panel-heading')
        # print(inner[0].text)

        txt = inner[0].text

        if(txt == "TWENTY20"):
            tab = curr.select('.table')
            print(tab[0].select('tfoot'))
            total = tab[0].select('tfoot')

            for data in total[0].select("td"):
                values.append(data.text)
                print(data.text)

            break

    res['Runs'] = values[1]
    res['Balls'] = values[2]
    res['Outs'] = values[3]
    res['Dots'] = values[4]
    res['Fours'] = values[5]
    res['Sixes'] = values[6]
    res['Strike Rate'] = values[7]

    return res

def index(request):
    players_list = ['SR Watson', 'F du Plessis', 'SK Raina', 'SR Watson', 'SK Raina', 'AT Rayudu', 'KL Rahul', 'CH Gayle', 'MA Agarwal', 'KK Nair', 'AJ Finch', 'AR Patel', 'AR Patel', 'AJ Finch', 'R Ashwin', 'AJ Tye', 'BB Sran', 'MM Sharma', 'RA Tripathi', 'JC Archer', 'AM Rahane', 'RA Tripathi', 'AM Rahane', 'SV Samson', 'H Klaasen', 'K Gowtham', 'JC Buttler', 'BA Stokes', 'P Chopra', 'P Chopra', 'STR Binny', 'JC Buttler', 'K Gowtham', 'S Dhawan', 'SP Goswami', 'KS Williamson', 'KS Williamson', 'MK Pandey', 'S Dhawan', 'YK Pathan', 'CR Brathwaite', 'Shakib Al Hasan', 'Rashid Khan', 'B Kumar', 'SA Yadav', 'E Lewis', 'Ishan Kishan', 'HH Pandya', 'Ishan Kishan', 'HH Pandya', 'RG Sharma', 'KH Pandya', 'S Dhawan', 'KS Williamson', 'WP Saha', 'MK Pandey', 'Shakib Al Hasan', 'YK Pathan', 'Mohammad Nabi', 'Rashid Khan', 'Rashid Khan', 'YK Pathan', 'Basil Thampi', 'S Kaul', 'Sandeep Sharma', 'CA Lynn', 'SP Narine', 'RV Uthappa', 'Shubman Gill', 'RK Singh', 'Shubman Gill', 'RK Singh', 'KD Karthik', 'Q de Kock', 'V Kohli', 'AB de Villiers', 'AB de Villiers', 'Q de Kock', 'CJ Anderson', 'Mandeep Singh', 'C de Grandhomme', 'P Negi', 'Washington Sundar', 'UT Yadav', 'SA Yadav', 'E Lewis', 'RG Sharma', 'Ishan Kishan', 'HH Pandya', 'BCJ Cutting', 'KH Pandya', 'AT Rayudu', 'F du Plessis', 'SK Raina', 'SW Billings', 'Harbhajan Singh', 'DL Chahar', 'SK Raina', 'DL Chahar', 'MS Dhoni', 'S Dhawan', 'AD Hales', 'KS Williamson', 'MK Pandey', 'DJ Hooda', 'Shakib Al Hasan', 'DJ Hooda', 'M Vohra', 'Q de Kock', 'BB McCullum', 'V Kohli', 'BB McCullum', 'V Kohli', 'Mandeep Singh', 'Washington Sundar', 'C de Grandhomme', 'TG Southee', 'UT Yadav', 'CA Lynn', 'SP Narine', 'RV Uthappa', 'N Rana', 'KD Karthik', 'Shubman Gill', 'Shubman Gill', 'KD Karthik', 'AD Russell', 'Shivam Mavi', 'PP Chawla', 'MG Johnson', 'Kuldeep Yadav', 'Q de Kock', 'M Vohra', 'V Kohli', 'AB de Villiers', 'V Kohli', 'PP Shaw', 'GJ Maxwell', 'SS Iyer', 'RR Pant', 'RR Pant', 'SS Iyer', 'NV Ojha', 'V Shankar', 'DT Christian', 'KA Pollard', 'A Dananjaya', 'M Markande', 'AM Rahane', 'RA Tripathi', 'SV Samson', 'BA Stokes', 'BA Stokes', 'SV Samson', 'JC Buttler', 'JC Archer', 'H Klaasen', 'K Gowtham', 'KL Rahul', 'CH Gayle', 'AJ Finch', 'KL Rahul', 'MP Stoinis', 'Yuvraj Singh', 'MK Tiwary', 'SA Yadav', 'E Lewis', 'SR Watson', 'MS Dhoni', 'DJ Bravo', 'DJ Bravo', 'F du Plessis', 'RA Jadeja', 'DL Chahar', 'Harbhajan Singh', 'SN Thakur', 'AM Rahane', 'K Gowtham', 'JC Buttler', 'SV Samson', 'BA Stokes', 'STR Binny', 'MK Lomror', 'JC Archer', 'JD Unadkat', 'RK Bhui', 'MK Pandey', 'KS Williamson', 'DJ Hooda', 'Shakib Al Hasan', 'Shakib Al Hasan', 'KS Williamson', 'YK Pathan', 'WP Saha', 'Rashid Khan', 'KL Rahul', 'MA Agarwal', 'AJ Finch', 'Yuvraj Singh', 'KK Nair', 'MP Stoinis', 'R Ashwin', 'AJ Tye', 'MM Sharma', 'Mujeeb Ur Rahman', 'SA Yadav', 'E Lewis', 'JP Duminy', 'KL Rahul', 'KL Rahul', 'CH Gayle', 'MA Agarwal', 'SA Yadav', 'E Lewis', 'RG Sharma', 'HH Pandya', 'SR Watson', 'F du Plessis', 'SR Watson', 'F du Plessis', 'SK Raina', 'AT Rayudu', 'MS Dhoni', 'PP Shaw', 'GJ Maxwell', 'SS Iyer', 'RR Pant', 'SS Iyer', 'RR Pant', 'V Shankar', 'Abhishek Sharma', 'AD Hales', 'S Dhawan', 'KS Williamson', 'PP Shaw', 'SS Iyer', 'RR Pant', 'RR Pant', 'SS Iyer', 'GJ Maxwell', 'V Shankar', 'Abhishek Sharma', 'HV Patel', 'PA Patel', 'MM Ali', 'V Kohli', 'AB de Villiers', 'V Kohli', 'AB de Villiers', 'Mandeep Singh', 'SN Khan', 'C de Grandhomme', 'S Dhawan', 'KS Williamson', 'WP Saha', 'MK Pandey', 'Shakib Al Hasan', 'MK Pandey', 'Mohammad Nabi', 'DJM Short', 'JC Buttler', 'SV Samson', 'BA Stokes', 'RA Tripathi', 'K Gowtham', 'MA Agarwal', 'KK Nair', 'DA Miller', 'AJ Tye', 'SR Watson', 'AT Rayudu', 'SK Raina', 'DR Shorey', 'MS Dhoni', 'SP Narine', 'RV Uthappa', 'CA Lynn', 'CA Lynn', 'RV Uthappa', 'N Rana', 'KD Karthik', 'Shubman Gill', 'AD Russell', 'JPR Scantlebury-Searles', 'V Kohli', 'PA Patel', 'YK Pathan', 'WP Saha', 'Rashid Khan', 'SR Watson', 'AT Rayudu', 'SK Raina', 'SR Watson', 'MS Dhoni', 'SW Billings', 'DJ Bravo', 'DJ Bravo', 'RA Jadeja', 'KK Nair', 'AR Patel', 'MP Stoinis', 'WP Saha', 'S Dhawan', 'KS Williamson', 'MK Pandey', 'Shakib Al Hasan', 'DJ Hooda', 'YK Pathan', 'DJ Hooda', 'YK Pathan', 'Rashid Khan', 'S Kaul', 'Sandeep Sharma', 'B Stanlake', 'RV Uthappa', 'CA Lynn', 'N Rana', 'SP Narine', 'KD Karthik', 'AD Russell', 'AD Russell', 'KD Karthik', 'Shubman Gill', 'Shivam Mavi', 'MG Johnson', 'CA Lynn', 'SP Narine', 'RV Uthappa', 'N Rana', 'RK Singh', 'AD Russell', 'KD Karthik', 'TK Curran', 'SR Watson', 'M Vijay', 'AT Rayudu', 'SW Billings', 'MS Dhoni', 'RA Jadeja', 'DJ Bravo', 'C Munro', 'G Gambhir', 'SS Iyer', 'V Shankar', 'RR Pant', 'G Gambhir', 'R Tewatia', 'CH Morris', 'DT Christian', 'N Rana', 'V Kohli', 'Q de Kock', 'AB de Villiers', 'Mandeep Singh', 'SN Khan', 'CR Woakes', 'Mohammed Siraj', 'BB McCullum', 'AB de Villiers', 'SN Khan', 'CR Woakes', 'G Gambhir', 'JJ Roy', 'SS Iyer', 'RR Pant', 'GJ Maxwell', 'R Tewatia', 'CH Morris', 'Mohammed Shami', 'S Nadeem', 'TA Boult', 'AM Rahane', 'RA Tripathi', 'SV Samson', 'JC Buttler', 'K Gowtham', 'S Gopal', 'DS Kulkarni', 'JD Unadkat', 'B Laughlin', 'DJ Hooda', 'CR Brathwaite', 'B Kumar', 'DJM Short', 'SV Samson', 'BA Stokes', 'JC Buttler', 'JC Buttler', 'SV Samson', 'RA Tripathi', 'GJ Maxwell', 'CH Morris', 'PA Patel', 'M Vohra', 'MM Ali', 'KK Nair', 'CH Gayle', 'AJ Finch', 'Q de Kock', 'BB McCullum', 'V Kohli', 'M Vohra', 'Mandeep Singh', 'V Kohli', 'Mandeep Singh', 'C de Grandhomme', 'MS Dhoni', 'KM Jadhav', 'RA Jadeja', 'DJ Bravo', 'DL Chahar', 'Harbhajan Singh', 'MA Wood', 'Imran Tahir', 'Imran Tahir', 'DJ Bravo', 'KM Jadhav', 'Rashid Khan', 'WP Saha', 'S Kaul', 'B Kumar', 'Sandeep Sharma', 'AB de Villiers', 'P Negi', 'Washington Sundar', 'Washington Sundar', 'CR Woakes', 'Mandeep Singh', 'RG Sharma', 'E Lewis', 'Ishan Kishan', 'SA Yadav', 'HH Pandya', 'KH Pandya', 'KH Pandya', 'HH Pandya', 'WP Saha', 'MK Pandey', 'DJ Hooda', 'Shakib Al Hasan', 'SP Narine', 'STR Binny', 'JD Unadkat', 'IS Sodhi', 'JC Archer', 'Anureet Singh', 'Anureet Singh', 'JD Unadkat', 'N Rana', 'KD Karthik', 'AD Russell', 'Shubman Gill', 'PP Chawla', 'PP Chawla', 'Shubman Gill', 'Shivam Mavi', 'Kuldeep Yadav', 'SP Narine', 'CA Lynn', 'RV Uthappa', 'N Rana', 'KD Karthik', 'RK Singh', 'AD Russell', 'AD Russell', 'KD Karthik', 'R Vinay Kumar', 'RG Sharma', 'KA Pollard', 'HH Pandya', 'MJ McClenaghan', 'CA Lynn', 'SP Narine', 'RV Uthappa', 'N Rana', 'Shubman Gill', 'TK Curran', 'PP Chawla', 'CH Gayle', 'SR Watson', 'AT Rayudu', 'RA Jadeja', 'DJM Short', 'AM Rahane', 'DJM Short', 'SV Samson', 'RA Tripathi', 'BA Stokes', 'JC Buttler', 'K Gowtham', 'S Gopal', 'DS Kulkarni', 'MA Agarwal', 'Yuvraj Singh', 'KK Nair', 'DA Miller', 'MP Stoinis', 'SV Samson', 'AM Rahane', 'BA Stokes', 'MK Lomror', 'JC Archer', 'H Klaasen', 'STR Binny', 'S Gopal', 'JD Unadkat', 'B Laughlin', 'S Dhawan', 'KS Williamson', 'S Dhawan', 'MK Pandey', 'Shakib Al Hasan', 'DJ Hooda', 'YK Pathan', 'JC Buttler', 'AM Rahane', 'SV Samson', 'JC Buttler', 'BA Stokes', 'RA Tripathi', 'JC Archer', 'K Gowtham', 'S Gopal', 'JD Unadkat', 'RG Sharma', 'E Lewis', 'Ishan Kishan', 'KA Pollard', 'BCJ Cutting', 'PJ Sangwan', 'JJ Bumrah', 'M Markande', 'H Klaasen', 'STR Binny', 'KL Rahul', 'KK Nair', 'CH Gayle', 'MP Stoinis', 'AJ Finch', 'MA Agarwal', 'AR Patel', 'R Ashwin', 'AJ Tye', 'MM Sharma', 'AS Rajpoot', 'PP Shaw', 'GJ Maxwell', 'LE Plunkett', 'KK Nair', 'MA Agarwal', 'AJ Finch', 'MK Tiwary', 'R Ashwin', 'AJ Tye', 'BB Sran', 'AS Rajpoot', 'Mujeeb Ur Rahman', 'PA Patel', 'BB McCullum', 'V Kohli', 'AB de Villiers', 'Mandeep Singh', 'C de Grandhomme', 'M Ashwin', 'TG Southee', 'UT Yadav', 'Mohammed Siraj', 'PP Shaw', 'G Gambhir', 'DT Christian', 'R Tewatia', 'LE Plunkett', 'A Mishra', 'PP Shaw', 'HV Patel', 'Ishan Kishan', 'Ishan Kishan', 'KA Pollard', 'RG Sharma', 'BCJ Cutting', 'M Markande', 'JJ Bumrah', 'PP Shaw', 'JJ Roy', 'SW Billings', 'RA Jadeja', 'DJ Bravo', 'DL Chahar', 'BB McCullum', 'SN Khan', 'CR Woakes', 'Washington Sundar', 'Shubman Gill', 'C Munro', 'C Munro', 'V Shankar', 'R Tewatia', 'CA Lynn', 'SP Narine', 'RV Uthappa', 'N Rana', 'Shubman Gill', 'PP Chawla', 'SK Raina', 'DJ Bravo', 'DJM Short', 'AM Rahane', 'KA Pollard', 'BCJ Cutting', 'MJ McClenaghan', 'M Markande', 'AD Nath', 'MK Tiwary', 'SP Goswami', 'SP Goswami', 'YK Pathan', 'CR Brathwaite', 'B Kumar', 'SP Goswami', 'DJ Hooda', 'CR Brathwaite', 'PP Shaw', 'C Munro', 'JJ Roy', 'G Gambhir', 'JJ Roy', 'G Gambhir', 'SS Iyer', 'RR Pant', 'GJ Maxwell', 'R Tewatia', 'JP Duminy', 'KA Pollard', 'KH Pandya', 'HH Pandya', 'BCJ Cutting', 'SA Yadav', 'E Lewis', 'Ishan Kishan', 'KA Pollard', 'RG Sharma', 'KH Pandya', 'MJ McClenaghan', 'M Markande', 'AD Hales', 'JJ Roy', 'G Gambhir', 'JJ Roy', 'MK Tiwary', 'DA Miller', 'AS Rajpoot', 'SP Narine', 'CA Lynn', 'RV Uthappa', 'N Rana', 'RK Singh', 'Kuldeep Yadav', 'M Prasidh Krishna', 'PA Patel', 'MM Ali', 'C de Grandhomme', 'SN Khan', 'TG Southee', 'SA Yadav', 'E Lewis', 'Ishan Kishan', 'KH Pandya', 'MJ McClenaghan', 'JJ Bumrah', 'Mustafizur Rahman', 'CH Gayle', 'SK Raina', 'SW Billings', 'RA Jadeja', 'MS Dhoni', 'F du Plessis', 'SK Raina', 'MS Dhoni', 'AT Rayudu', 'RA Jadeja', 'AB de Villiers', 'MM Ali', 'Mandeep Singh', 'C de Grandhomme', 'C de Grandhomme', 'AB de Villiers', 'SN Khan', 'TG Southee', 'UT Yadav', 'Mohammed Siraj', 'YS Chahal', 'CA Lynn', 'SP Narine', 'RV Uthappa', 'AD Russell', 'KD Karthik', 'KD Karthik', 'AD Russell', 'JPR Scantlebury-Searles', 'AM Rahane', 'JC Buttler', 'SV Samson', 'SPD Smith', 'RA Tripathi', 'BA Stokes', 'R Parag', 'JC Archer', 'S Gopal', 'KL Rahul', 'CH Gayle', 'MA Agarwal', 'DA Miller', 'N Pooran', 'N Pooran', 'DA Miller', 'Mandeep Singh', 'R Ashwin', 'GC Viljoen', 'M Ashwin', 'Q de Kock', 'SD Lad', 'SA Yadav', 'KA Pollard', 'Ishan Kishan', 'HH Pandya', 'KA Pollard', 'HH Pandya', 'KH Pandya', 'AS Joseph', 'RD Chahar', 'KL Rahul', 'CH Gayle', 'MA Agarwal', 'DA Miller', 'KL Rahul', 'DA Miller', 'N Pooran', 'Mandeep Singh', 'R Ashwin', 'Mujeeb Ur Rahman', 'CA Lynn', 'SP Narine', 'Shubman Gill', 'RV Uthappa', 'N Rana', 'AD Russell', 'AD Russell', 'N Rana', 'DA Warner', 'JM Bairstow', 'KS Williamson', 'RK Bhui', 'RK Bhui', 'DA Warner', 'V Shankar', 'Abhishek Sharma', 'DJ Hooda', 'Rashid Khan', 'B Kumar', 'Sandeep Sharma', 'KK Ahmed', 'KL Rahul', 'CH Gayle', 'MA Agarwal', 'SM Curran', 'Mandeep Singh', 'R Ashwin', 'Harpreet Brar', 'GC Viljoen', 'AM Rahane', 'JC Buttler', 'SV Samson', 'SV Samson', 'SPD Smith', 'RA Tripathi', 'LS Livingstone', 'K Gowtham', 'S Gopal', 'AM Rahane', 'BA Stokes', 'BA Stokes', 'AM Rahane', 'AJ Turner', 'STR Binny', 'R Parag', 'V Kohli', 'PA Patel', 'MM Ali', 'AB de Villiers', 'SO Hetmyer', 'S Dube', 'C de Grandhomme', 'NA Saini', 'YS Chahal', 'UT Yadav', 'UT Yadav', 'PA Patel', 'Mohammed Siraj', 'DA Warner', 'WP Saha', 'MK Pandey', 'Mohammad Nabi', 'KS Williamson', 'KS Williamson', 'Mohammad Nabi', 'Rashid Khan', 'V Shankar', 'Abhishek Sharma', 'V Kohli', 'AB de Villiers', 'MP Stoinis', 'H Klaasen', 'Gurkeerat Singh', 'PA Patel', 'P Negi', 'NA Saini', 'SR Watson', 'AT Rayudu', 'SK Raina', 'KM Jadhav', 'MS Dhoni', 'KM Jadhav', 'MS Dhoni', 'RA Jadeja', 'DJ Bravo', 'DL Chahar', 'SN Thakur', 'MM Sharma', 'AT Rayudu', 'SR Watson', 'SK Raina', 'SK Raina', 'MS Dhoni', 'DJ Bravo', 'RA Jadeja', 'PP Shaw', 'S Dhawan', 'SS Iyer', 'SS Iyer', 'S Dhawan', 'RR Pant', 'CA Ingram', 'KMA Paul', 'AR Patel', 'R Tewatia', 'AB de Villiers', 'V Kohli', 'S Dube', 'H Klaasen', 'Gurkeerat Singh', 'MP Stoinis', 'Washington Sundar', 'PA Patel', 'MM Ali', 'PA Patel', 'V Kohli', 'AB de Villiers', 'SO Hetmyer', 'C de Grandhomme', 'S Dube', 'MP Stoinis', 'MM Ali', 'PP Shaw', 'S Dhawan', 'SS Iyer', 'RR Pant', 'CA Ingram', 'GH Vihari', 'PA Patel', 'V Kohli', 'AB de Villiers', 'PA Patel', 'AD Nath', 'MP Stoinis', 'MM Ali', 'P Negi', 'UT Yadav', 'V Kohli', 'AB de Villiers', 'CA Lynn', 'SP Narine', 'Shubman Gill', 'N Rana', 'KD Karthik', 'KD Karthik', 'CA Lynn', 'RK Singh', 'AD Russell', 'PP Chawla', 'Y Prithvi Raj', 'KC Cariappa', 'SR Watson', 'F du Plessis', 'SK Raina', 'AT Rayudu', 'KM Jadhav', 'MS Dhoni', 'RA Jadeja', 'JM Bairstow', 'JM Bairstow', 'YK Pathan', 'MK Pandey', 'SV Samson', 'SPD Smith', 'SR Watson', 'F du Plessis', 'SK Raina', 'SK Raina', 'SR Watson', 'AT Rayudu', 'KM Jadhav', 'F du Plessis', 'JL Denly', 'RV Uthappa', 'Shubman Gill', 'KD Karthik', 'CR Brathwaite', 'PP Chawla', 'Kuldeep Yadav', 'AM Rahane', 'LS Livingstone', 'AJ Turner', 'KL Rahul', 'CH Gayle', 'KL Rahul', 'CH Gayle', 'MA Agarwal', 'DA Miller', 'DA Warner', 'JM Bairstow', 'JM Bairstow', 'DA Warner', 'KS Williamson', 'V Shankar', 'MK Pandey', 'Rashid Khan', 'YK Pathan', 'F du Plessis', 'SK Raina', 'MS Dhoni', 'RA Jadeja', 'AT Rayudu', 'Shubman Gill', 'CA Lynn', 'N Rana', 'RV Uthappa', 'AD Russell', 'KD Karthik', 'JM Bairstow', 'DA Warner', 'DA Warner', 'JM Bairstow', 'V Shankar', 'MK Pandey', 'DJ Hooda', 'YK Pathan', 'Mohammad Nabi', 'JC Buttler', 'PP Shaw', 'S Dhawan', 'SS Iyer', 'CA Ingram', 'RR Pant', 'CH Morris', 'R Tewatia', 'AR Patel', 'RG Sharma', 'Q de Kock', 'SA Yadav', 'Q de Kock', 'SA Yadav', 'KA Pollard', 'Yuvraj Singh', 'HH Pandya', 'KH Pandya', 'BCJ Cutting', 'MJ McClenaghan', 'Rasikh Salam', 'RG Sharma', 'E Lewis', 'E Lewis', 'RG Sharma', 'KH Pandya', 'V Shankar', 'Mohammad Nabi', 'MK Pandey', 'DJ Hooda', 'PP Shaw', 'S Dhawan', 'S Dhawan', 'PP Shaw', 'C Munro', 'SS Iyer', 'RR Pant', 'AR Patel', 'CH Morris', 'A Mishra', 'K Rabada', 'CH Morris', 'HV Patel', 'Avesh Khan', 'K Rabada', 'S Lamichhane', 'DA Warner', 'JM Bairstow', 'KS Williamson', 'CA Lynn', 'N Rana', 'Shubman Gill', 'KD Karthik', 'SP Narine', 'CR Brathwaite', 'RK Singh', 'JC Buttler', 'SPD Smith', 'RA Tripathi', 'BA Stokes', 'DA Warner', 'JM Bairstow', 'YK Pathan', 'Rashid Khan', 'B Kumar', 'Sandeep Sharma', 'S Kaul', 'SN Khan', 'SN Khan', 'SM Curran', 'JC Buttler', 'AM Rahane', 'SV Samson', 'SPD Smith', 'RA Tripathi', 'BA Stokes', 'K Gowtham', 'JC Archer', 'JD Unadkat', 'S Gopal', 'DS Kulkarni', 'KL Rahul', 'MA Agarwal', 'SM Curran', 'SN Khan', 'SN Khan', 'MA Agarwal', 'DA Miller', 'Mandeep Singh', 'GC Viljoen', 'R Ashwin', 'M Ashwin', 'Mohammed Shami', 'N Pooran', 'SA Yadav', 'Q de Kock', 'Ishan Kishan', 'SR Watson', 'F du Plessis', 'SR Watson', 'SW Billings', 'RA Jadeja', 'CA Lynn', 'SP Narine', 'SP Narine', 'CA Lynn', 'RV Uthappa', 'Shubman Gill', 'AM Rahane', 'SV Samson', 'SPD Smith', 'BA Stokes', 'R Parag', 'R Parag', 'STR Binny', 'JC Archer', 'JD Unadkat', 'SO Hetmyer', 'M Vijay', 'SR Watson', 'SK Raina', 'AT Rayudu', 'KM Jadhav', 'DR Shorey', 'DR Shorey', 'M Vijay', 'DJ Bravo', 'MJ Santner', 'DL Chahar', 'Harbhajan Singh', 'RG Sharma', 'BCJ Cutting', 'SS Iyer', 'CA Ingram', 'CA Ingram', 'S Dhawan', 'RR Pant', 'KMA Paul', 'AR Patel', 'R Tewatia', 'AD Nath', 'TG Southee', 'P Negi', 'Mohammed Siraj', 'YS Chahal', 'RR Pant', 'CA Lynn', 'SP Narine', 'RV Uthappa', 'N Rana', 'KD Karthik', 'Shubman Gill', 'AD Russell', 'PP Chawla', 'Kuldeep Yadav', 'M Prasidh Krishna', 'HF Gurney', 'MK Pandey', 'V Shankar', 'YK Pathan', 'CH Gayle', 'MA Agarwal', 'MA Agarwal', 'CH Gayle', 'SN Khan', 'SM Curran', 'Mandeep Singh', 'SR Watson', 'F du Plessis', 'SK Raina', 'AT Rayudu', 'KM Jadhav', 'MS Dhoni', 'MS Dhoni', 'DJ Bravo', 'N Rana', 'RV Uthappa', 'KD Karthik', 'AD Russell', 'Shubman Gill', 'PP Chawla', 'KS Williamson', 'SN Khan', 'PP Shaw', 'S Dhawan', 'SS Iyer', 'RR Pant', 'R Tewatia', 'CA Ingram', 'SS Iyer', 'CH Morris', 'K Rabada', 'SO Hetmyer', 'C de Grandhomme', 'P Ray Barman', 'P Ray Barman', 'C de Grandhomme', 'Mohammed Siraj', 'YS Chahal', 'SE Rutherford', 'J Suchith', 'J Suchith', 'A Mishra', 'TA Boult', 'BB Sran', 'RD Chahar', 'Yuvraj Singh', 'MJ McClenaghan', 'JC Buttler', 'Shakib Al Hasan', 'WP Saha', 'KM Jadhav', 'AT Rayudu', 'C Munro', 'CH Morris', 'K Rabada', 'PP Shaw', 'RR Pant', 'SE Rutherford', 'CA Ingram', 'RG Sharma', 'Q de Kock', 'SA Yadav', 'KA Pollard', 'Q de Kock', 'HH Pandya', 'Ishan Kishan', 'KK Nair', 'KL Rahul', 'KK Nair', 'SM Curran', 'Mandeep Singh', 'MP Stoinis', 'F du Plessis', 'MS Dhoni', 'AT Rayudu', 'MS Dhoni', 'AT Rayudu', 'MS Dhoni', 'RA Jadeja', 'PA Patel', 'V Kohli', 'AD Nath', 'MM Ali', 'RA Tripathi', 'JC Buttler', 'SV Samson', 'RA Tripathi', 'SV Samson', 'AM Rahane', 'AJ Turner', 'JC Archer', 'STR Binny', 'S Gopal', 'Q de Kock', 'RG Sharma', 'SA Yadav', 'M Markande', 'JJ Bumrah', 'NS Naik', 'KD Karthik', 'Shubman Gill', 'AD Russell', 'PP Chawla', 'Kuldeep Yadav', 'CA Lynn', 'SP Narine', 'RV Uthappa', 'CA Lynn', 'Shubman Gill', 'RA Tripathi', 'K Gowtham', 'JC Archer', 'S Gopal', 'Q de Kock', 'SA Yadav', 'RG Sharma', 'Yuvraj Singh', 'KH Pandya', 'HH Pandya', 'KA Pollard', 'SR Watson', 'SR Watson', 'SK Raina', 'KM Jadhav', 'DJ Bravo', 'N Pooran', 'R Ashwin', 'P Simran Singh', 'Mujeeb Ur Rahman', 'Mohammed Shami', 'M Ashwin', 'SV Samson', 'LS Livingstone']

    players_list = list(set(players_list))
    
    if request.method == "GET":
        context_data = {
            'players': players_list
        }
    else:
        player1 = request.POST.get('batsman')
        player2 = request.POST.get('bowler')

        data = {}

        try:
            data = getStats(player1, player2)
        except IndexError as e:
            sweetify.success(request, 'Data not found', text='The record for selected player was not found', button='OK')

        context_data = {
            "data": data,
            "players": players_list,
            "player1": player1,
            "player2": player2           
        }

    return render(request, 'dashboard.html', context_data)


def toss_graph(matches, delivery):
    df = matches.iloc[[matches['win_by_runs'].idxmax()]]
    mlt.subplots(figsize=(10,6))
    sns.countplot(x='season',hue='toss_decision',data=matches)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'toss_graph.png')
    plt.savefig(imageFile, format='png')
    plt.clf()

def toss_win_match_win(matches, delivery):
    df = matches[matches['toss_winner']==matches['winner']]
    slices = [len(df),(577-len(df))]
    labels = ['Yes','No']
    mlt.pie(slices,labels=labels,startangle=90,shadow=True,explode=(0,0.05),autopct='%1.1f%%',colors=['r','g'])
    fig = mlt.gcf()
    fig.set_size_inches(6,6)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats', 'ipl', 'toss_win_match_win.png')
    plt.savefig(imageFile, format='png')
    fig.clf()

def team1_vs_team2(team1,team2, matches):
    mt1 = matches[((matches['team1']==team1)|(matches['team2']==team1))&((matches['team1']==team2)|(matches['team2']==team2))]
    sns.countplot(x='season', hue='winner', data=mt1, palette='Set3')
    mlt.xticks(rotation='vertical')
    leg = mlt.legend( loc = 'upper center')
    fig=mlt.gcf()
    fig.set_size_inches(18,8)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'ipl', 'team1_team2.png')
    plt.savefig(imageFile, format='png')

def batting_bowling(delivery):
    high_scores=delivery.groupby(['match_id', 'inning','batting_team','bowling_team'])['total_runs'].sum().reset_index() 
    high_scores=high_scores[high_scores['total_runs']>=200]
    high_scores.nlargest(10,'total_runs')

    fig, ax = mlt.subplots(1,2)
    sns.countplot(high_scores['batting_team'],ax=ax[0])
    sns.countplot(high_scores['bowling_team'],ax=ax[1])
    mlt.xticks(rotation=90)
    fig=mlt.gcf()
    fig.set_size_inches(18,8)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'ipl', 'batting_bowling.png')
    plt.savefig(imageFile, format='png')
    fig.clf()

def team_chasing(delivery):
    high_scores=delivery.groupby(['match_id', 'inning','batting_team','bowling_team'])['total_runs'].sum().reset_index()
    high_scores1=high_scores[high_scores['inning']==1]
    high_scores2=high_scores[high_scores['inning']==2]
    high_scores1=high_scores1.merge(high_scores2[['match_id','inning', 'total_runs']], on='match_id')
    high_scores1.rename(columns={'inning_x':'inning_1','inning_y':'inning_2','total_runs_x':'inning1_runs','total_runs_y':'inning2_runs'},inplace=True)
    high_scores1=high_scores1[high_scores1['inning1_runs']>=200]
    high_scores1['is_score_chased']=1
    high_scores1['is_score_chased'] = np.where(high_scores1['inning1_runs']<=high_scores1['inning2_runs'], 
                                            'yes', 'no')

    slices=high_scores1['is_score_chased'].value_counts().reset_index().is_score_chased
    labels=['target not chased','target chased']
    mlt.pie(slices,labels=labels,colors=['#1f2ff3', '#0fff00'],startangle=90,shadow=True,explode=(0,0.1),autopct='%1.1f%%')
    fig = mlt.gcf()
    fig.set_size_inches(6,6)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'ipl', 'team_chasing.png')
    plt.savefig(imageFile, format='png')
    fig.clf()

def top_batsmen(delivery):
    toppers=delivery.groupby(['batsman','batsman_runs'])['total_runs'].count().reset_index()
    toppers=toppers.pivot('batsman','batsman_runs','total_runs')
    fig,ax=mlt.subplots(2,2,figsize=(18,12))
    toppers[1].sort_values(ascending=False)[:5].plot(kind='barh',ax=ax[0,0],color='#45ff45',width=0.8)
    ax[0,0].set_title("Most 1's")
    ax[0,0].set_ylabel('')
    toppers[2].sort_values(ascending=False)[:5].plot(kind='barh',ax=ax[0,1],color='#df6dfd',width=0.8)
    ax[0,1].set_title("Most 2's")
    ax[0,1].set_ylabel('')
    toppers[4].sort_values(ascending=False)[:5].plot(kind='barh',ax=ax[1,0],color='#fbca5f',width=0.8)
    ax[1,0].set_title("Most 4's")
    ax[1,0].set_ylabel('')
    toppers[6].sort_values(ascending=False)[:5].plot(kind='barh',ax=ax[1,1],color='#ffff00',width=0.8)
    ax[1,1].set_title("Most 6's")
    ax[1,1].set_ylabel('')
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'ipl', 'top_batsmen.png')
    plt.savefig(imageFile, format='png')
    fig.clf()

def top_batsmen_score(matches, delivery):
    max_runs=delivery.groupby(['batsman'])['batsman_runs'].sum()
    batsmen = matches[['id','season']].merge(delivery, left_on = 'id', right_on = 'match_id', how = 'left').drop('id', axis = 1)
    a=batsmen.groupby(['batsman','batsman_runs'])['total_runs'].count().reset_index()
    b=max_runs.sort_values(ascending=False)[:10].reset_index()
    c=b.merge(a,left_on='batsman',right_on='batsman',how='left')
    c.drop('batsman_runs_x',axis=1,inplace=True)
    c.set_index('batsman',inplace=True)
    c.columns=['type','count']
    c=c[(c['type']==1)|(c['type']==2)|(c['type']==4)|(c['type']==6)]
    cols=['type','count']
    c.reset_index(inplace=True)
    c=c.pivot('batsman','type','count')

    trace1 = go.Bar(
        y=c.index, x=c[6],
        name="6's",
        orientation = 'h',
        marker = dict(color = 'rgba(178, 78, 139, 0.6)',
            line = dict(color = 'rgba(178, 78, 139, 1.0)',
                width = 3)
        )
    )
    trace2 = go.Bar(
        y=c.index, x=c[4],
        name="4's",
        orientation = 'h',
        marker = dict(color = 'rgba(58, 71, 80, 0.6)',
            line = dict(color = 'rgba(58, 71, 80, 1.0)',
                width = 3)
        )
    )

    trace3 = go.Bar(
        y=c.index, x=c[2],
        name="2's",
        orientation = 'h',
        marker = dict(color = 'rgba(101, 178, 139, 0.6)',
            line = dict(color = 'rgba(101, 178, 139, 1.0)',
                width = 3)
        )
    )
    trace4 = go.Bar(
        y=c.index, x=c[1],
        name="1's",
        orientation = 'h',
        marker = dict(color = 'rgba(208, 105, 80, 0.6)',
            line = dict(color = 'rgba(208, 105, 80, 1.0)',
                width = 3)
        )
    )

    data = [trace1, trace2,trace3,trace4]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=data, layout=layout)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'ipl', 'top_batsmen_score.png')
    fig.write_image(imageFile)
    

def ipl_index(request):
    matches_data = os.path.join(settings.BASE_DIR, 'data', 'matches.csv')
    deliveries_data = os.path.join(settings.BASE_DIR, 'data', 'deliveries.csv')

    matches = pd.read_csv(matches_data)   
    delivery = pd.read_csv(deliveries_data)

    matches.drop(['umpire3'], axis=1, inplace=True)
    delivery.fillna(0,inplace=True)

    matches.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors','Rising Pune Supergiant']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','RPS'],inplace=True)

    delivery.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors','Rising Pune Supergiant']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','RPS'],inplace=True)
    
    # toss_win_match_win(matches, delivery)
    toss_graph(matches, delivery)
    batting_bowling(delivery)
    team_chasing(delivery)
    top_batsmen(delivery)
    # top_batsmen_score(matches, delivery)

    teams =  ['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','RPS']

    context_data = {
        'teams' : teams
    }

    return render(request, 'ipl/dashboard.html', context_data)


def setTeam(request):
    if request.method == 'POST':
        team = request.POST.get('team')
        context_data = {
            'team_name': team
        }
        return render(request, 'dashboard.html', context_data)

def get_teams_stats(request):

    team1 = request.POST.get('team1')
    team2 = request.POST.get('team2')

    matches_data = os.path.join(settings.BASE_DIR, 'data', 'matches.csv')
    deliveries_data = os.path.join(settings.BASE_DIR, 'data', 'deliveries.csv')

    matches = pd.read_csv(matches_data)   
    delivery = pd.read_csv(deliveries_data)

    matches.drop(['umpire3'], axis=1, inplace=True)
    delivery.fillna(0,inplace=True)

    matches.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors','Rising Pune Supergiant']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','RPS'],inplace=True)

    delivery.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors','Rising Pune Supergiant']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','RPS'],inplace=True)
    
    team1_vs_team2(team1,team2, matches)

    return HttpResponseRedirect('/ipl/')
    