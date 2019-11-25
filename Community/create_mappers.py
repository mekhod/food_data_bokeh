import pickle

string_states = """01 AL 30 MT 02 AK 31 NE 04 AZ 32 NV 05 AR 33 NH 06 CA 34 NJ 08 CO 35 NM 09 CT 36 NY 10 DE 37 NC 11 DC 38 ND 12 FL 39 OH 13 GA 40 OK 15 HI 41 OR 16 ID 42 PA 17 IL 44 RI 18 IN 45 SC 19 IA 46 SD 20 KS 47 TN 21 KY 48 TX 22 LA 49 UT 23 ME 50 VT 24 MD 51 VA 25 MA 53 WA 26 MI 54 WV 27 MN 55 WI 28 MS 56 WY 29 MO"""

list_string_states = string_states.split(" ")

mapper_state_code = {}

while True:
    try:
        mapper_state_code[list_string_states.pop()] = list_string_states.pop()
    except:
        break

text_metro_1 = """10180 Abilene, TX 10420 Akron, OH 10580 Albany-Schenectady-Troy, NY 10740 Albuquerque, NM 10900 Allentown-Bethlehem-Easton, PA-NJ 11100 Amarillo, TX 11460 Ann Arbor, MI 11540 Appleton, WI 11700 Asheville, NC 12020 Athens-Clarke County, GA 12060 Atlanta-Sandy Springs-Roswell, GA 12100 Atlantic City-Hammonton, NJ 12220 Auburn-Opelika, AL 12260 Augusta-Richmond County, GA-SC 12420 Austin-Round Rock, TX 12540 Bakersfield, CA 12580 Baltimore-Columbia-Towson, MD 12620 Bangor, ME 12700 Barnstable, MA 12940 Baton Rouge, LA 12980 Battle Creek, MI 13140 Beaumont-Port Arthur, TX 13460 Bend-Redmond, OR 13740 Billings, MT 13780 Binghamton, NY 13820 Birmingham-Hoover, AL 13980 Blacksburg—Christiansburg-Radford, VA 14010 Bloomington, IL 14020 Bloomington, IN 14260 Boise City, ID 14460 Boston-Cambridge-Newton, MA-NH 14500 Boulder, CO 14540 Bowling Green, KY 14860 Bridgeport-Stamford-Norwalk, CT"""
text_metro_2 = """ 15180 Brownsville-Harlingen, TX 15380 Buffalo-Cheektowaga-Niagara Falls, NY 15500 Burlington, NC 15540 Burlington-South Burlington, VT 15680 California-Lexington Park, MD 15940 Canton-Massillon, OH 15980 Cape Coral-Fort Myers, FL 16060 Carbondale-Marion, IL 16300 Cedar Rapids, IA 16540 Chambersburg-Waynesboro, PA 16580 Champaign-Urbana, IL 16620 Charleston, WV 16700 Charleston-North Charleston, SC 16740 Charlotte-Concord-Gastonia, NC-SC 16820 Charlottesville, VA 16860 Chattanooga, TN-GA 16980 Chicago-Naperville-Elgin, IL-IN-WI 17020 Chico, CA 17140 Cincinnati, OH-KY-IN 17300 Clarksville, TN-KY 17420 Cleveland, TN 17460 Cleveland-Elyria, OH 17660 Coeur d’Alene, ID 17780 College Station-Bryan, TX 17820 Colorado Springs, CO 17900 Columbia, SC 17980 Columbus, GA-AL 18140 Columbus, OH 18580 Corpus Christi, TX 19100 Dallas-Fort Worth-Arlington, TX 19300 Daphne-Fairhope-Foley, AL 19340 Davenport-Moline-Rock Island, IA-IL 19380 Dayton, OH 19660 Deltona-Daytona Beach-Ormond Beach, FL 19740 Denver-Aurora-Lakewood, CO 19780 Des Moines-West Des Moines, IA 19820 Detroit-Warren-Dearborn, MI 20100 Dover, DE 20500 Durham-Chapel Hill, NC 20700 East Stroudsburg, PA"""
text_metro_3 = """ 21140 Elkhart-Goshen, IN 21340 El Paso, TX 21500 Erie, PA 21660 Eugene, OR 21780 Evansville, IN-KY 22020 Fargo, ND-MN 22140 Farmington, NM 22180 Fayetteville, NC 22220 Fayetteville-Springdale-Rogers, AR-MO 22420 Flint, MI 22500 Florence, SC 22520 Florence-Muscle Shoals, AL 22660 Fort Collins, CO 22900 Fort Smith, AR-OK 23060 Fort Wayne, IN 23420 Fresno, CA 23540 Gainesville, FL 23580 Gainesville, GA 24020 Glen Falls, NY 24140 Goldsboro, NC 24340 Grand Rapids-Wyoming, MI 24540 Greeley, CO 24580 Green Bay, WI 24660 Greensboro-High Point, NC 24780 Greenville, NC 24860 Greenville-Anderson-Mauldin, SC 25180 Hagerstown-Martinsburg, MD-WV 25260 Hanford-Corcoran, CA 25420 Harrisburg-Carlisle, PA 25540 Hartford-West Hartford-East Hartford, CT 25860 Hickory-Morganton-Lenoir, NC 25940 Hilton Head Island-Bluffton-Beaufort, SC 26420 Houston-Baytown-Sugar Land, TX 26580 Huntington-Ashland, WV-KY-OH 26620 Huntsville, AL 26820 Idaho Falls, ID 26900 Indianapolis, IN 26980 Iowa City, IA 27100 Jackson, MI 27140 Jackson, MS"""
text_metro_4 = """ 27260 Jacksonville, FL 27340 Jacksonville, NC 27500 Janesville-Beloit, WI 27740 Johnson City, TN 27780 Johnstown, PA 27980 Kahului-Wailuku-Lahaina, HI 28020 Kalamazoo-Portage, MI 28140 Kansas City, MO-KS 28420 Kennewick-Richland, WA 28660 Killeen-Temple-Fort Hood, TX 28700 Kingsport-Bristol, TN-VA 28940 Knoxville, TN 29180 Lafayette, LA 29200 Lafayette-West Lafayette, IN 29340 Lake Charles, LA 29460 Lakeland-Winter Haven, FL 29540 Lancaster, PA 29620 Lansing-East Lansing, MI 29700 Laredo, TX 29740 Las Cruces, NM 29820 Las Vegas-Paradise, NV 30340 Lewiston-Auburn, ME 30460 Lexington-Fayette, KY 30780 Little Rock-North Little Rock, AR 30980 Longview, TX 31080 Los Angeles-Long Beach-Anaheim, CA 31140 Louisville, KY-IN 31180 Lubbock, TX 31420 Macon, GA 31540 Madison, WI 31700 Manchester-Nashua, NH 32580 McAllen-Edinburg-Mission, TX 32780 Medford, OR 32820 Memphis, TN-MS-AR 33100 Miami-Fort Lauderdale-West Palm Beach, FL 33340 Milwaukee-Waukesha-West Allis, WI 33460 Minneapolis-St Paul-Bloomington, MN-WI 33660 Mobile, AL 33700 Modesto, CA 33740 Monroe, LA"""
text_metro_5 = """ 33780 Monroe, MI 33860 Montgomery, AL 34060 Morgantown, WV 34580 Mount Vernon-Anacortes, WA 34740 Muskegon-Norton Shores, MI 34820 Myrtle Beach-Conway-North Myrtle Beach, SC-NC 34940 Naples-Immokalee-Marco Island, FL 34980 Nashville-Davidson-Murfreesboro, TN 35300 New Haven-Milford, CT 35380 New Orleans-Metairie, LA 35620 New York-Newark- Jersey City, NY-NJ-PA (White Plains central city recoded to balance of metropolitan) 35660 Niles-Benton Harbor, MI 35840 North Port-Sarasota-Bradenton, FL 35980 Norwich-New London, CT 36100 Ocala, FL 36220 Odessa, TX 36260 Ogden-Clearfield, UT 36420 Oklahoma City, OK 36540 Omaha-Council Bluffs, NE-IA 36740 Orlando, FL 36780 Oshkosh-Neenah, WI 37100 Oxnard-Thousand Oaks-Ventura, CA 37340 Palm Bay-Melbourne-Titusville, FL 37460 Panama City, FL 37860 Pensacola-Ferry Pass-Brent, FL 37900 Peoria, IL 37980 Philadelphia-Camden-Wilmington, PA-NJ-DE 38060 Phoenix-Mesa-Scottsdale, AZ 38220 Pine Bluff, AR 38300 Pittsburgh, PA 38860 Portland-South Portland, ME 38900 Portland-Vancouver-Hillsboro, OR-WA 38940 Port St. Lucie-Fort Pierce, FL 39140 Prescott, AZ 39300 Providence-Warwick, RI-MA 39340 Provo-Orem, UT 39540 Racine, WI 39580 Raleigh, NC 39740 Reading, PA"""
text_metro_6 = """ 39820 Redding, CA 40060 Richmond, VA 40140 Riverside-San Bernardino-Ontario, CA 40220 Roanoke, VA 40380 Rochester, NY 40420 Rockford, IL 40900 Sacramento--Arden-Arcade–Roseville, CA 40980 Saginaw, MI 41100 St. George, UT 41180 St. Louis, MO-IL 41420 Salem, OR 41500 Salinas, CA 41540 Salisbury, MD 41620 Salt Lake City, UT 41700 San Antonio, TX 41740 San Diego-Carlsbad-San Marcos, CA 41860 San Francisco-Oakland-Fremont, CA 41940 San Jose-Sunnyvale-Santa Clara, CA 42020 San Luis Obispo-Paso Robles, CA 42100 Santa Cruz-Watsonville, CA 42140 Santa Fe, NM 42200 Santa Maria-Santa Barbara, CA 42220 Santa Rosa-Petaluma, CA 42340 Savannah, GA 42540 Scranton--Wilkes-Barre, PA 42660 Seattle-Tacoma-Bellevue, WA 43300 Sherman-Dennison, TX 43340 Shreveport-Bossier City, LA 43620 Sioux Falls, SD 43780 South Bend-Mishawaka, IN-MI 43900 Spartanburg, SC 44060 Spokane-Spokane Valley, WA 44100 Springfield, IL 44140 Springfield, MA 44180 Springfield, MO 44700 Stockton-Lodi, CA 45060 Syracuse, NY 45220 Tallahassee, FL 45300 Tampa-St. Petersburg-Clearwater, FL 45460 Terre Haute, IN"""
text_metro_7 = """ 45780 Toledo, OH 45820 Topeka, KS 45940 Trenton, NJ 46060 Tucson, AZ 46140 Tulsa, OK 46340 Tyler, TX 46520 Urban Honolulu, HI 46540 Utica-Rome, NY 46700 Vallejo-Fairfield, CA 47220 Vineland-Bridgeton, NJ 47260 Virginia Beach-Norfolk-Newport News, VA-NC 47300 Visalia-Porterville, CA 47380 Waco, TX 47580 Warner Robins, GA 47900 Washington-Arlington-Alexandria, DC-VA-MD-WV 47940 Waterloo-Cedar Falls, IA 48060 Watertown-Fort Drum, NY 48140 Wausau, WI 48620 Wichita, KS 48660 Wichita Falls, TX 48700 Williamsport, PA 49020 Winchester, VA-WV 49180 Winston-Salem, NC 49340 Worcester, MA-CT 49620 York-Hanover, PA 49660 Youngstown-Warren-Boardman, OH-PA 49740 Yuma, AZ"""

text_metro = text_metro_1 + text_metro_2 + text_metro_3 + text_metro_4 + text_metro_5 + text_metro_6 + text_metro_7

new_text_metro = ''
prev_digit = False
for i in range(len(text_metro)):

    try:
        l = int(text_metro[i + 1])
        if not prev_digit:
            new_text_metro += ':'
        new_text_metro += text_metro[i]
        prev_digit = True
    except:
        new_text_metro += text_metro[i]
        if prev_digit:
            new_text_metro += ':'
            prev_digit = False

new_text_metro = new_text_metro[1:]

list_metro = new_text_metro.split(':')

list_metro = [i.strip() for i in list_metro]

mapper_metro = {}
while True:
    try:
        mapper_metro[list_metro.pop()] = list_metro.pop()
    except:
        break

mapper_metro['00000'] = 'NOT IDENTIFIED OR NONMETROPOLITAN'

#####################################
mapper_age_range = {'1': 'child', '2': 'adult', '3': 'adult_armed_forces'}

mapper_interview_type = {'1': 'interview',
                         '2': 'type_A_noninterview',
                         '3': 'type_B_noninterview',
                         '4': 'type_C_noninterview'}

mapper_state_code = {'29': 'MO', '56': 'WY', '28': 'MS', '55': 'WI', '27': 'MN', '54': 'WV', '26': 'MI',
                     '53': 'WA', '25': 'MA', '51': 'VA', '24': 'MD', '50': 'VT', '23': 'ME', '49': 'UT',
                     '22': 'LA', '48': 'TX', '21': 'KY', '47': 'TN', '20': 'KS', '46': 'SD', '19': 'IA',
                     '45': 'SC', '18': 'IN', '44': 'RI', '17': 'IL', '42': 'PA', '16': 'ID', '41': 'OR',
                     '15': 'HI', '40': 'OK', '13': 'GA', '39': 'OH', '12': 'FL', '38': 'ND', '11': 'DC',
                     '37': 'NC', '10': 'DE', '36': 'NY', '09': 'CT', '35': 'NM', '08': 'CO', '34': 'NJ',
                     '06': 'CA', '33': 'NH', '05': 'AR', '32': 'NV', '04': 'AZ', '31': 'NE', '02': 'AK',
                     '30': 'MT', '01': 'AL'}

mapper_registered_type = {'1': 'yes', '2': 'no',
                          '-1': 'not_in_universe',
                          '-2': 'not_know', '-3': 'refused',
                          '-9': 'no_response'}

mapper_voting_type = {'1': 'yes', '2': 'no',
                      '-1': 'not_in_universe',
                      '-2': 'not_know', '-3': 'refused',
                      '-9': 'no_response'}

mapper_education_type = {'31': 'LESS THAN 1ST GRADE',
                         '32': '1ST, 2ND, 3RD OR 4TH GRADE',
                         '33': '5TH OR 6TH GRADE',
                         '34': '7TH OR 8TH GRADE',
                         '35': '9TH GRADE',
                         '36': '10TH GRADE',
                         '37': '11TH GRADE',
                         '38': '12TH GRADE NO DIPLOMA',
                         '39': 'HIGH SCHOOL GRAD-DIPLOMA OR EQUIV (GED)',
                         '40': 'SOME COLLEGE BUT NO DEGREE',
                         '41': 'ASSOCIATE DEGREE-OCCUPATIONAL/VOCATIONAL',
                         '42': 'ASSOCIATEDEGREE-ACADEMICPROGRAM',
                         '43': "BACHELOR'S DEGREE (EX: BA, AB, BS)",
                         "44": "MASTER'S DEGREE (EX:MA,MS,MEng,MEd, MSW)",
                         "45": "PROFESSIONAL SCHOOL DEG (EX:MD, DDS, DVM)",
                         "46": "DOCTORATE DEGREE (EX: PhD, EdD)"}

##############################
mappers_all = {'mapper_metro': mapper_metro,
               'mapper_age_range': mapper_age_range,
               'mapper_interview_type': mapper_interview_type,
               'mapper_state_code': mapper_state_code,
               'mapper_registered_type': mapper_registered_type,
               'mapper_voting_type': mapper_voting_type,
               'mapper_education_type': mapper_education_type}

################################
with open('data/Community_Context/mappers.pkl', 'wb') as f:
    pickle.dump(mappers_all, f)
