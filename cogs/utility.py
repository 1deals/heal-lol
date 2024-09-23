import discord
import sys
import aiohttp

from tools.managers.context import Context
from discord.ext.commands import (
    command,
    group,
    BucketType,
    cooldown,
    has_permissions,
    hybrid_command,
    hybrid_group,
)
from tools.configuration import Emojis, Colors
from tools.paginator import Paginator
from discord.utils import format_dt
from discord.ext import commands
from tools.heal import Heal
from discord.ui import View, Button
from typing import Union, List
from datetime import datetime, timedelta
import humanize
import datetime
import requests
import io, re
from discord import Message
import shazamio
from shazamio import Shazam, Serialize
from PIL import Image, ImageDraw, ImageFont
import random
from random import choice
from tools.managers.embedBuilder import EmbedBuilder, EmbedScript
from tools.configuration import api
from io import BytesIO
from rembg import remove
import google.generativeai as genai
from tools.managers.flags import ScriptFlags
from discord import AllowedMentions
import pytz
from pytz import timezone

all_timezones = pytz.all_timezones


TIMEZONEMAPPING = {
    'Abidjan': 'Africa/Abidjan',
    'Accra': 'Africa/Accra',
    'Addis Ababa': 'Africa/Addis_Ababa',
    'Algiers': 'Africa/Algiers',
    'Asmara': 'Africa/Asmara',
    'Asmera': 'Africa/Asmera',
    'Bamako': 'Africa/Bamako',
    'Bangui': 'Africa/Bangui',
    'Banjul': 'Africa/Banjul',
    'Bissau': 'Africa/Bissau',
    'Blantyre': 'Africa/Blantyre',
    'Brazzaville': 'Africa/Brazzaville',
    'Bujumbura': 'Africa/Bujumbura',
    'Cairo': 'Africa/Cairo',
    'Casablanca': 'Africa/Casablanca',
    'Ceuta': 'Africa/Ceuta',
    'Conakry': 'Africa/Conakry',
    'Dakar': 'Africa/Dakar',
    'Dar es Salaam': 'Africa/Dar_es_Salaam',
    'Djibouti': 'Africa/Djibouti',
    'Douala': 'Africa/Douala',
    'El_Aaiun': 'Africa/El_Aaiun',
    'Freetown': 'Africa/Freetown',
    'Gaborone': 'Africa/Gaborone',
    'Harare': 'Africa/Harare',
    'Johannesburg': 'Africa/Johannesburg',
    'Juba': 'Africa/Juba',
    'Kampala': 'Africa/Kampala',
    'Khartoum': 'Africa/Khartoum',
    'Kigali': 'Africa/Kigali',
    'Kinshasa': 'Africa/Kinshasa',
    'Lagos': 'Africa/Lagos',
    'Libreville': 'Africa/Libreville',
    'Lome': 'Africa/Lome',
    'Luanda': 'Africa/Luanda',
    'Lubumbashi': 'Africa/Lubumbashi',
    'Lusaka': 'Africa/Lusaka',
    'Malabo': 'Africa/Malabo',
    'Maputo': 'Africa/Maputo',
    'Maseru': 'Africa/Maseru',
    'Mbabane': 'Africa/Mbabane',
    'Mogadishu': 'Africa/Mogadishu',
    'Monrovia': 'Africa/Monrovia',
    'Nairobi': 'Africa/Nairobi',
    'Ndjamena': 'Africa/Ndjamena',
    'Niamey': 'Africa/Niamey',
    'Nouakchott': 'Africa/Nouakchott',
    'Ouagadougou': 'Africa/Ouagadougou',
    'Porto-Novo': 'Africa/Porto-Novo',
    'Sao Tome': 'Africa/Sao_Tome',
    'Timbuktu': 'Africa/Timbuktu',
    'Tripoli': 'Africa/Tripoli',
    'Tunis': 'Africa/Tunis',
    'Windhoek': 'Africa/Windhoek',
    'Adak': 'America/Adak',
    'Anchorage': 'America/Anchorage',
    'Anguilla': 'America/Anguilla',
    'Antigua': 'America/Antigua',
    'Araguaina': 'America/Araguaina',
    'Buenos_Aires': 'America/Argentina/Buenos_Aires',
    'Catamarca': 'America/Argentina/Catamarca',
    'ComodRivadavia': 'America/Argentina/ComodRivadavia',
    'Cordoba': 'America/Argentina/Cordoba',
    'Jujuy': 'America/Argentina/Jujuy',
    'La Rioja': 'America/Argentina/La_Rioja',
    'Mendoza': 'America/Argentina/Mendoza',
    'Rio Gallegos': 'America/Argentina/Rio_Gallegos',
    'Salta': 'America/Argentina/Salta',
    'San Juan': 'America/Argentina/San_Juan',
    'San Luis': 'America/Argentina/San_Luis',
    'Tucuman': 'America/Argentina/Tucuman',
    'Ushuaia': 'America/Argentina/Ushuaia',
    'Aruba': 'America/Aruba',
    'Asuncion': 'America/Asuncion',
    'Atikokan': 'America/Atikokan',
    'Atka': 'America/Atka',
    'Bahia': 'America/Bahia',
    'Bahia Banderas': 'America/Bahia_Banderas',
    'Barbados': 'America/Barbados',
    'Belem': 'America/Belem',
    'Belize': 'America/Belize',
    'Blanc-Sablon': 'America/Blanc-Sablon',
    'Boa Vista': 'America/Boa_Vista',
    'Bogota': 'America/Bogota',
    'Boise': 'America/Boise',
    'Cambridge Bay': 'America/Cambridge_Bay',
    'Campo Grande': 'America/Campo_Grande',
    'Cancun': 'America/Cancun',
    'Caracas': 'America/Caracas',
    'Cayenne': 'America/Cayenne',
    'Cayman': 'America/Cayman',
    'Chicago': 'America/Chicago',
    'Chihuahua': 'America/Chihuahua',
    'Ciudad Juarez': 'America/Ciudad_Juarez',
    'Coral Harbour': 'America/Coral_Harbour',
    'Cordoba': 'America/Cordoba',
    'Costa Rica': 'America/Costa_Rica',
    'Creston': 'America/Creston',
    'Cuiaba': 'America/Cuiaba',
    'Curacao': 'America/Curacao',
    'Danmarkshavn': 'America/Danmarkshavn',
    'Dawson': 'America/Dawson',
    'Dawson Creek': 'America/Dawson_Creek',
    'Denver': 'America/Denver',
    'Detroit': 'America/Detroit',
    'Dominica': 'America/Dominica',
    'Edmonton': 'America/Edmonton',
    'Eirunepe': 'America/Eirunepe',
    'El Salvador': 'America/El_Salvador',
    'Ensenada': 'America/Ensenada',
    'Fort Nelson': 'America/Fort_Nelson',
    'Fort Wayne': 'America/Fort_Wayne',
    'Fortaleza': 'America/Fortaleza',
    'Glace Bay': 'America/Glace_Bay',
    'Godthab': 'America/Godthab',
    'Goose Bay': 'America/Goose_Bay',
    'Grand Turk': 'America/Grand_Turk',
    'Grenada': 'America/Grenada',
    'Guadeloupe': 'America/Guadeloupe',
    'Guatemala': 'America/Guatemala',
    'Guayaquil': 'America/Guayaquil',
    'Guyana': 'America/Guyana',
    'Halifax': 'America/Halifax',
    'Havana': 'America/Havana',
    'Hermosillo': 'America/Hermosillo',
    'Indiana/Indianapolis': 'America/Indiana/Indianapolis',
    'Indiana/Knox': 'America/Indiana/Knox',
    'Indiana/Marengo': 'America/Indiana/Marengo',
    'Indiana/Petersburg': 'America/Indiana/Petersburg',
    'Indiana/Tell City': 'America/Indiana/Tell_City',
    'Indiana/Vevay': 'America/Indiana/Vevay',
    'Indiana/Vincennes': 'America/Indiana/Vincennes',
    'Indiana/Winamac': 'America/Indiana/Winamac',
    'Indianapolis': 'America/Indianapolis',
    'Inuvik': 'America/Inuvik',
    'Iqaluit': 'America/Iqaluit',
    'Jamaica': 'America/Jamaica',
    'Jujuy': 'America/Jujuy',
    'Juneau': 'America/Juneau',
    'Kentucky/Louisville': 'America/Kentucky/Louisville',
    'Kentucky/Monticello': 'America/Kentucky/Monticello',
    'Knox IN': 'America/Knox_IN',
    'Kralendijk': 'America/Kralendijk',
    'La Paz': 'America/La_Paz',
    'Lima': 'America/Lima',
    'Los Angeles': 'America/Los_Angeles',
    'Louisville': 'America/Louisville',
    'Lower Princes': 'America/Lower_Princes',
    'Maceio': 'America/Maceio',
    'Managua': 'America/Managua',
    'Manaus': 'America/Manaus',
    'Marigot': 'America/Marigot',
    'Martinique': 'America/Martinique',
    'Matamoros': 'America/Matamoros',
    'Mazatlan': 'America/Mazatlan',
    'Mendoza': 'America/Mendoza',
    'Menominee': 'America/Menominee',
    'Merida': 'America/Merida',
    'Metlakatla': 'America/Metlakatla',
    'Mexico City': 'America/Mexico_City',
    'Miquelon': 'America/Miquelon',
    'Moncton': 'America/Moncton',
    'Monterrey': 'America/Monterrey',
    'Montevideo': 'America/Montevideo',
    'Montreal': 'America/Montreal',
    'Montserrat': 'America/Montserrat',
    'Nassau': 'America/Nassau',
    'New York': 'America/New_York',
    'Nipigon': 'America/Nipigon',
    'Nome': 'America/Nome',
    'Noronha': 'America/Noronha',
    'North Dakota/Beulah': 'America/North_Dakota/Beulah',
    'North Dakota/Center': 'America/North_Dakota/Center',
    'North Dakota/New_Salem': 'America/North_Dakota/New_Salem',
    'Nuuk': 'America/Nuuk',
    'Ojinaga': 'America/Ojinaga',
    'Panama': 'America/Panama',
    'Pangnirtung': 'America/Pangnirtung',
    'Paramaribo': 'America/Paramaribo',
    'Phoenix': 'America/Phoenix',
    'Port au Prince': 'America/Port-au-Prince',
    'Port of Spain': 'America/Port_of_Spain',
    'Porto Acre': 'America/Porto_Acre',
    'Porto Velho': 'America/Porto_Velho',
    'Puerto Rico': 'America/Puerto_Rico',
    'Punta Arenas': 'America/Punta_Arenas',
    'Rainy River': 'America/Rainy_River',
    'Rankin Inlet': 'America/Rankin_Inlet',
    'Recife': 'America/Recife',
    'Regina': 'America/Regina',
    'Resolute': 'America/Resolute',
    'Rio Branco': 'America/Rio_Branco',
    'Rosario': 'America/Rosario',
    'Santa Isabel': 'America/Santa_Isabel',
    'Santarem': 'America/Santarem',
    'Santiago': 'America/Santiago',
    'Santo Domingo': 'America/Santo_Domingo',
    'Sao Paulo': 'America/Sao_Paulo',
    'Scoresbysund': 'America/Scoresbysund',
    'Shiprock': 'America/Shiprock',
    'Sitka': 'America/Sitka',
    'St Barthelemy': 'America/St_Barthelemy',
    'St Johns': 'America/St_Johns',
    'St Kitts': 'America/St_Kitts',
    'St Lucia': 'America/St_Lucia',
    'St Thomas': 'America/St_Thomas',
    'St Vincent': 'America/St_Vincent',
    'Swift Current': 'America/Swift_Current',
    'Tegucigalpa': 'America/Tegucigalpa',
    'Thule': 'America/Thule',
    'Thunder Bay': 'America/Thunder_Bay',
    'Tijuana': 'America/Tijuana',
    'Toronto': 'America/Toronto',
    'Tortola': 'America/Tortola',
    'Vancouver': 'America/Vancouver',
    'Virgin': 'America/Virgin',
    'Whitehorse': 'America/Whitehorse',
    'Winnipeg': 'America/Winnipeg',
    'Yakutat': 'America/Yakutat',
    'Yellowknife': 'America/Yellowknife',
    'Casey': 'Antarctica/Casey',
    'Davis': 'Antarctica/Davis',
    'DumontDUrville': 'Antarctica/DumontDUrville',
    'Macquarie': 'Antarctica/Macquarie',
    'Mawson': 'Antarctica/Mawson',
    'McMurdo': 'Antarctica/McMurdo',
    'Palmer': 'Antarctica/Palmer',
    'Rothera': 'Antarctica/Rothera',
    'South Pole': 'Antarctica/South_Pole',
    'Syowa': 'Antarctica/Syowa',
    'Troll': 'Antarctica/Troll',
    'Vostok': 'Antarctica/Vostok',
    'Longyearbyen': 'Arctic/Longyearbyen',
    'Aden': 'Asia/Aden',
    'Almaty': 'Asia/Almaty',
    'Amman': 'Asia/Amman',
    'Anadyr': 'Asia/Anadyr',
    'Aqtau': 'Asia/Aqtau',
    'Aqtobe': 'Asia/Aqtobe',
    'Ashgabat': 'Asia/Ashgabat',
    'Ashkhabad': 'Asia/Ashkhabad',
    'Atyrau': 'Asia/Atyrau',
    'Baghdad': 'Asia/Baghdad',
    'Bahrain': 'Asia/Bahrain',
    'Baku': 'Asia/Baku',
    'Bangkok': 'Asia/Bangkok',
    'Barnaul': 'Asia/Barnaul',
    'Beirut': 'Asia/Beirut',
    'Bishkek': 'Asia/Bishkek',
    'Brunei': 'Asia/Brunei',
    'Calcutta': 'Asia/Calcutta',
    'Chita': 'Asia/Chita',
    'Choibalsan': 'Asia/Choibalsan',
    'Chongqing': 'Asia/Chongqing',
    'Chungking': 'Asia/Chungking',
    'Colombo': 'Asia/Colombo',
    'Dacca': 'Asia/Dacca',
    'Damascus': 'Asia/Damascus',
    'Dhaka': 'Asia/Dhaka',
    'Dili': 'Asia/Dili',
    'Dubai': 'Asia/Dubai',
    'Dushanbe': 'Asia/Dushanbe',
    'Famagusta': 'Asia/Famagusta',
    'Gaza': 'Asia/Gaza',
    'Harbin': 'Asia/Harbin',
    'Hebron': 'Asia/Hebron',
    'Ho Chi Minh': 'Asia/Ho_Chi_Minh',
    'Hong Kong': 'Asia/Hong_Kong',
    'Hovd': 'Asia/Hovd',
    'Irkutsk': 'Asia/Irkutsk',
    'Istanbul': 'Asia/Istanbul',
    'Jakarta': 'Asia/Jakarta',
    'Jayapura': 'Asia/Jayapura',
    'Jerusalem': 'Asia/Jerusalem',
    'Kabul': 'Asia/Kabul',
    'Kamchatka': 'Asia/Kamchatka',
    'Karachi': 'Asia/Karachi',
    'Kashgar': 'Asia/Kashgar',
    'Kathmandu': 'Asia/Kathmandu',
    'Katmandu': 'Asia/Katmandu',
    'Khandyga': 'Asia/Khandyga',
    'Kolkata': 'Asia/Kolkata',
    'Krasnoyarsk': 'Asia/Krasnoyarsk',
    'Kuala Lumpur': 'Asia/Kuala_Lumpur',
    'Kuching': 'Asia/Kuching',
    'Kuwait': 'Asia/Kuwait',
    'Macao': 'Asia/Macao',
    'Macau': 'Asia/Macau',
    'Magadan': 'Asia/Magadan',
    'Makassar': 'Asia/Makassar',
    'Manila': 'Asia/Manila',
    'Muscat': 'Asia/Muscat',
    'Nicosia': 'Asia/Nicosia',
    'Novokuznetsk': 'Asia/Novokuznetsk',
    'Novosibirsk': 'Asia/Novosibirsk',
    'Omsk': 'Asia/Omsk',
    'Oral': 'Asia/Oral',
    'Phnom Penh': 'Asia/Phnom_Penh',
    'Pontianak': 'Asia/Pontianak',
    'Pyongyang': 'Asia/Pyongyang',
    'Qatar': 'Asia/Qatar',
    'Qostanay': 'Asia/Qostanay',
    'Qyzylorda': 'Asia/Qyzylorda',
    'Rangoon': 'Asia/Rangoon',
    'Riyadh': 'Asia/Riyadh',
    'Saigon': 'Asia/Saigon',
    'Sakhalin': 'Asia/Sakhalin',
    'Samarkand': 'Asia/Samarkand',
    'Seoul': 'Asia/Seoul',
    'Shanghai': 'Asia/Shanghai',
    'Singapore': 'Asia/Singapore',
    'Srednekolymsk': 'Asia/Srednekolymsk',
    'Taipei': 'Asia/Taipei',
    'Tashkent': 'Asia/Tashkent',
    'Tbilisi': 'Asia/Tbilisi',
    'Tehran': 'Asia/Tehran',
    'Tel Aviv': 'Asia/Tel_Aviv',
    'Thimbu': 'Asia/Thimbu',
    'Thimphu': 'Asia/Thimphu',
    'Tokyo': 'Asia/Tokyo',
    'Tomsk': 'Asia/Tomsk',
    'Ujung Pandang': 'Asia/Ujung_Pandang',
    'Ulaanbaatar': 'Asia/Ulaanbaatar',
    'Ulan Bator': 'Asia/Ulan_Bator',
    'Urumqi': 'Asia/Urumqi',
    'Ust Nera': 'Asia/Ust-Nera',
    'Vientiane': 'Asia/Vientiane',
    'Vladivostok': 'Asia/Vladivostok',
    'Yakutsk': 'Asia/Yakutsk',
    'Yangon': 'Asia/Yangon',
    'Yekaterinburg': 'Asia/Yekaterinburg',
    'Yerevan': 'Asia/Yerevan',
    'Azores': 'Atlantic/Azores',
    'Bermuda': 'Atlantic/Bermuda',
    'Canary': 'Atlantic/Canary',
    'Cape Verde': 'Atlantic/Cape_Verde',
    'Faeroe': 'Atlantic/Faeroe',
    'Faroe': 'Atlantic/Faroe',
    'Jan Mayen': 'Atlantic/Jan_Mayen',
    'Madeira': 'Atlantic/Madeira',
    'Reykjavik': 'Atlantic/Reykjavik',
    'South Georgia': 'Atlantic/South_Georgia',
    'St Helena': 'Atlantic/St_Helena',
    'Stanley': 'Atlantic/Stanley',
    'ACT': 'Australia/ACT',
    'Adelaide': 'Australia/Adelaide',
    'Brisbane': 'Australia/Brisbane',
    'Broken Hill': 'Australia/Broken_Hill',
    'Canberra': 'Australia/Canberra',
    'Currie': 'Australia/Currie',
    'Darwin': 'Australia/Darwin',
    'Eucla': 'Australia/Eucla',
    'Hobart': 'Australia/Hobart',
    'LHI': 'Australia/LHI',
    'Lindeman': 'Australia/Lindeman',
    'Lord Howe': 'Australia/Lord_Howe',
    'Melbourne': 'Australia/Melbourne',
    'NSW': 'Australia/NSW',
    'North': 'Australia/North',
    'Perth': 'Australia/Perth',
    'Queensland': 'Australia/Queensland',
    'South': 'Australia/South',
    'Sydney': 'Australia/Sydney',
    'Tasmania': 'Australia/Tasmania',
    'Victoria': 'Australia/Victoria',
    'West': 'Australia/West',
    'Yancowinna': 'Australia/Yancowinna',
    'Acre': 'Brazil/Acre',
    'DeNoronha': 'Brazil/DeNoronha',
    'East': 'Brazil/East',
    'West': 'Brazil/West',
    'CET': 'CET',
    'CST6CDT': 'CST6CDT',
    'Atlantic': 'Canada/Atlantic',
    'Central': 'Canada/Central',
    'Eastern': 'Canada/Eastern',
    'Mountain': 'Canada/Mountain',
    'Newfoundland': 'Canada/Newfoundland',
    'Pacific': 'Canada/Pacific',
    'Saskatchewan': 'Canada/Saskatchewan',
    'Yukon': 'Canada/Yukon',
    'Continental': 'Chile/Continental',
    'EasterIsland': 'Chile/EasterIsland',
    'Cuba': 'Cuba',
    'EET': 'EET',
    'EST': 'EST',
    'EST5EDT': 'EST5EDT',
    'Egypt': 'Egypt',
    'Eire': 'Eire',
    'GMT': 'Etc/GMT',
    'GMT+0': 'Etc/GMT+0',
    'GMT+1': 'Etc/GMT+1',
    'GMT+10': 'Etc/GMT+10',
    'GMT+11': 'Etc/GMT+11',
    'GMT+12': 'Etc/GMT+12',
    'GMT+2': 'Etc/GMT+2',
    'GMT+3': 'Etc/GMT+3',
    'GMT+4': 'Etc/GMT+4',
    'GMT+5': 'Etc/GMT+5',
    'GMT+6': 'Etc/GMT+6',
    'GMT+7': 'Etc/GMT+7',
    'GMT+8': 'Etc/GMT+8',
    'GMT+9': 'Etc/GMT+9',
    'GMT-0': 'Etc/GMT-0',
    'GMT-1': 'Etc/GMT-1',
    'GMT-10': 'Etc/GMT-10',
    'GMT-11': 'Etc/GMT-11',
    'GMT-12': 'Etc/GMT-12',
    'GMT-13': 'Etc/GMT-13',
    'GMT-14': 'Etc/GMT-14',
    'GMT-2': 'Etc/GMT-2',
    'GMT-3': 'Etc/GMT-3',
    'GMT-4': 'Etc/GMT-4',
    'GMT-5': 'Etc/GMT-5',
    'GMT-6': 'Etc/GMT-6',
    'GMT-7': 'Etc/GMT-7',
    'GMT-8': 'Etc/GMT-8',
    'GMT-9': 'Etc/GMT-9',
    'GMT0': 'Etc/GMT0',
    'Greenwich': 'Etc/Greenwich',
    'UCT': 'Etc/UCT',
    'UTC': 'Etc/UTC',
    'Universal': 'Etc/Universal',
    'Zulu': 'Etc/Zulu',
    'Amsterdam': 'Europe/Amsterdam',
    'Andorra': 'Europe/Andorra',
    'Astrakhan': 'Europe/Astrakhan',
    'Athens': 'Europe/Athens',
    'Belfast': 'Europe/Belfast',
    'Belgrade': 'Europe/Belgrade',
    'Berlin': 'Europe/Berlin',
    'Bratislava': 'Europe/Bratislava',
    'Brussels': 'Europe/Brussels',
    'Bucharest': 'Europe/Bucharest',
    'Budapest': 'Europe/Budapest',
    'Busingen': 'Europe/Busingen',
    'Chisinau': 'Europe/Chisinau',
    'Copenhagen': 'Europe/Copenhagen',
    'Dublin': 'Europe/Dublin',
    'Gibraltar': 'Europe/Gibraltar',
    'Guernsey': 'Europe/Guernsey',
    'Helsinki': 'Europe/Helsinki',
    'Isle of Man': 'Europe/Isle_of_Man',
    'Istanbul': 'Europe/Istanbul',
    'Jersey': 'Europe/Jersey',
    'Kaliningrad': 'Europe/Kaliningrad',
    'Kiev': 'Europe/Kiev',
    'Kirov': 'Europe/Kirov',
    'Kyiv': 'Europe/Kyiv',
    'Lisbon': 'Europe/Lisbon',
    'Ljubljana': 'Europe/Ljubljana',
    'London': 'Europe/London',
    'Luxembourg': 'Europe/Luxembourg',
    'Madrid': 'Europe/Madrid',
    'Malta': 'Europe/Malta',
    'Mariehamn': 'Europe/Mariehamn',
    'Minsk': 'Europe/Minsk',
    'Monaco': 'Europe/Monaco',
    'Moscow': 'Europe/Moscow',
    'Nicosia': 'Europe/Nicosia',
    'Oslo': 'Europe/Oslo',
    'Paris': 'Europe/Paris',
    'Podgorica': 'Europe/Podgorica',
    'Prague': 'Europe/Prague',
    'Riga': 'Europe/Riga',
    'Rome': 'Europe/Rome',
    'Samara': 'Europe/Samara',
    'San Marino': 'Europe/San_Marino',
    'Sarajevo': 'Europe/Sarajevo',
    'Saratov': 'Europe/Saratov',
    'Simferopol': 'Europe/Simferopol',
    'Skopje': 'Europe/Skopje',
    'Sofia': 'Europe/Sofia',
    'Stockholm': 'Europe/Stockholm',
    'Tallinn': 'Europe/Tallinn',
    'Tirane': 'Europe/Tirane',
    'Tiraspol': 'Europe/Tiraspol',
    'Ulyanovsk': 'Europe/Ulyanovsk',
    'Uzhgorod': 'Europe/Uzhgorod',
    'Vaduz': 'Europe/Vaduz',
    'Vatican': 'Europe/Vatican',
    'Vienna': 'Europe/Vienna',
    'Vilnius': 'Europe/Vilnius',
    'Volgograd': 'Europe/Volgograd',
    'Warsaw': 'Europe/Warsaw',
    'Zagreb': 'Europe/Zagreb',
    'Zaporozhye': 'Europe/Zaporozhye',
    'Zurich': 'Europe/Zurich',
    'GB': 'GB',
    'GB-Eire': 'GB-Eire',
    'GMT': 'GMT',
    'HST': 'HST',
    'Hongkong': 'Hongkong',
    'Iceland': 'Iceland',
    'Antananarivo': 'Indian/Antananarivo',
    'Chagos': 'Indian/Chagos',
    'Christmas': 'Indian/Christmas',
    'Cocos': 'Indian/Cocos',
    'Comoro': 'Indian/Comoro',
    'Kerguelen': 'Indian/Kerguelen',
    'Mahe': 'Indian/Mahe',
    'Maldives': 'Indian/Maldives',
    'Mauritius': 'Indian/Mauritius',
    'Mayotte': 'Indian/Mayotte',
    'Reunion': 'Indian/Reunion',
    'Iran': 'Iran',
    'Israel': 'Israel',
    'Jamaica': 'Jamaica',
    'Japan': 'Japan',
    'Kwajalein': 'Kwajalein',
    'Libya': 'Libya',
    'MET': 'MET',
    'MST': 'MST',
    'MST7MDT': 'MST7MDT',
    'BajaNorte': 'Mexico/BajaNorte',
    'BajaSur': 'Mexico/BajaSur',
    'General': 'Mexico/General',
    'NZ': 'NZ',
    'NZ-CHAT': 'NZ-CHAT',
    'Navajo': 'Navajo',
    'PRC': 'PRC',
    'PST8PDT': 'PST8PDT',
    'Apia': 'Pacific/Apia',
    'Auckland': 'Pacific/Auckland',
    'Bougainville': 'Pacific/Bougainville',
    'Chatham': 'Pacific/Chatham',
    'Chuuk': 'Pacific/Chuuk',
    'Easter': 'Pacific/Easter',
    'Efate': 'Pacific/Efate',
    'Enderbury': 'Pacific/Enderbury',
    'Fakaofo': 'Pacific/Fakaofo',
    'Fiji': 'Pacific/Fiji',
    'Funafuti': 'Pacific/Funafuti',
    'Galapagos': 'Pacific/Galapagos',
    'Gambier': 'Pacific/Gambier',
    'Guadalcanal': 'Pacific/Guadalcanal',
    'Guam': 'Pacific/Guam',
    'Honolulu': 'Pacific/Honolulu',
    'Johnston': 'Pacific/Johnston',
    'Kanton': 'Pacific/Kanton',
    'Kiritimati': 'Pacific/Kiritimati',
    'Kosrae': 'Pacific/Kosrae',
    'Kwajalein': 'Pacific/Kwajalein',
    'Majuro': 'Pacific/Majuro',
    'Marquesas': 'Pacific/Marquesas',
    'Midway': 'Pacific/Midway',
    'Nauru': 'Pacific/Nauru',
    'Niue': 'Pacific/Niue',
    'Norfolk': 'Pacific/Norfolk',
    'Noumea': 'Pacific/Noumea',
    'Pago_Pago': 'Pacific/Pago_Pago',
    'Palau': 'Pacific/Palau',
    'Pitcairn': 'Pacific/Pitcairn',
    'Pohnpei': 'Pacific/Pohnpei',
    'Ponape': 'Pacific/Ponape',
    'Port_Moresby': 'Pacific/Port_Moresby',
    'Rarotonga': 'Pacific/Rarotonga',
    'Saipan': 'Pacific/Saipan',
    'Samoa': 'Pacific/Samoa',
    'Tahiti': 'Pacific/Tahiti',
    'Tarawa': 'Pacific/Tarawa',
    'Tongatapu': 'Pacific/Tongatapu',
    'Truk': 'Pacific/Truk',
    'Wake': 'Pacific/Wake',
    'Wallis': 'Pacific/Wallis',
    'Yap': 'Pacific/Yap',
    'Poland': 'Poland',
    'Portugal': 'Portugal',
    'ROC': 'ROC',
    'ROK': 'ROK',
    'Singapore': 'Singapore',
    'Turkey': 'Turkey',
    'UCT': 'UCT',
    'US/Alaska': 'US/Alaska',
    'US/Aleutian': 'US/Aleutian',
    'US/Arizona': 'US/Arizona',
    'US/Central': 'US/Central',
    'US/East-Indiana': 'US/East-Indiana',
    'US/Eastern': 'US/Eastern',
    'US/Hawaii': 'US/Hawaii',
    'US/Indiana-Starke': 'US/Indiana-Starke',
    'US/Michigan': 'US/Michigan',
    'US/Mountain': 'US/Mountain',
    'US/Pacific': 'US/Pacific',
    'US/Samoa': 'US/Samoa',
    'UTC': 'UTC',
    'Universal': 'Universal',
    'W-SU': 'W-SU',
    'WET': 'WET',
    'Zulu': 'Zulu',
    'Makkah': 'Asia/Riyadh',
    'Saudi Arabia': 'Asia/Riyadh'
}

TIMEZONE_MAPPING = {tz: tz for tz in TIMEZONEMAPPING}


api_keys = [
    "AIzaSyARqu0-ecLbA5gTpcCi8R8n8DQnM_y5SCc",
    "AIzaSyD6kJ3BEfJ9MoyiqkGQqmKwCH41rSAI7OY",
    "AIzaSyB5M5n1Y6FbzJn8ArixxWBCfwBRMkJReNw",
]
key = random.choice(api_keys)
genai.configure(api_key=key)

model = genai.GenerativeModel("gemini-pro")


class Utility(commands.Cog):
    def __init__(self, bot: Heal) -> None:
        self.bot = bot
        self.deleted_messages = {}

    @commands.Cog.listener("on_message_edit")
    async def process_edits(
        self, before: discord.Message, after: discord.Message
    ) -> discord.Message:

        if before.content != after.content:
            await self.bot.process_commands(after)

    @hybrid_command(
        name="chatgpt",
        aliases=["openai", "ai", "ask", "askheal"],
        description="Ask chatgpt a question.",
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def chatgpt(self, ctx: Context, *, prompt: str):
        async with ctx.typing():
            response = model.generate_content(prompt)
            await ctx.reply(response.text)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.guild and not before.author.bot:
            channel_id = before.channel.id
            cached = await self.bot.cache.get(f"edited-{channel_id}")
            if cached is None:
                cached = []

            cached.append(
                {
                    "before_content": before.content,
                    "after_content": after.content,
                    "author": str(before.author),
                    "timestamp": (
                        before.edited_at.isoformat()
                        if before.edited_at
                        else before.created_at.isoformat()
                    ),
                }
            )

            await self.bot.cache.set(f"edited-{channel_id}", cached)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.guild:
            channel_id = message.channel.id

            cached_messages = await self.bot.cache.get(f"deleted_messages_{channel_id}")

            if cached_messages is None:
                cached_messages = []

            cached_messages.append(
                {
                    "content": message.content,
                    "author": str(message.author),
                    "timestamp": message.created_at.isoformat(),
                }
            )

            await self.bot.cache.set(f"deleted_messages_{channel_id}", cached_messages)

    @commands.command(aliases=["s"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def snipe(self, ctx: Context, index: int = 1):
        channel_id = ctx.channel.id

        sniped_messages = (
            await self.bot.cache.get(f"deleted_messages_{channel_id}") or []
        )

        if sniped_messages:
            if 1 <= index <= len(sniped_messages):
                deleted_message = sniped_messages[-index]

                message_user = ctx.guild.get_member_named(
                    deleted_message["author"]
                ) or ctx.guild.get_member(int(deleted_message["author"].split("#")[0]))

                if not message_user:
                    embed = discord.Embed(
                        description=f"> {Emojis.WARN} {ctx.author.mention}: User not found for the deleted message",
                        color=Colors.BASE_COLOR,
                    )
                    return await ctx.send(embed=embed)

                user_pfp = (
                    message_user.avatar.url
                    if message_user.avatar
                    else message_user.default_avatar.url
                )

                embed = discord.Embed(
                    title="",
                    description=deleted_message["content"],
                    color=Colors.BASE_COLOR,
                )
                embed.set_author(name=message_user.display_name, icon_url=user_pfp)
                embed.set_footer(text=f"Page {index} of {len(sniped_messages)}")

                await ctx.send(embed=embed)
            else:
                return await ctx.warn(f"Invalid snipe index")
        else:
            return await ctx.deny(f"No deleted messages to snipe")

    @commands.command(aliases=["es"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def editsnipe(self, ctx: Context, index: int = 1):
        channel_id = ctx.channel.id

        sniped_messages = await self.bot.cache.get(f"edited-{channel_id}") or []

        if sniped_messages:
            if 1 <= index <= len(sniped_messages):
                edited_message = sniped_messages[-index]

                message_user = ctx.guild.get_member_named(
                    edited_message["author"]
                ) or ctx.guild.get_member(int(edited_message["author"].split("#")[0]))

                if not message_user:
                    embed = discord.Embed(
                        description=f"> {Emojis.WARN} {ctx.author.mention}: User not found for the edited message",
                        color=Colors.BASE_COLOR,
                    )
                    return await ctx.send(embed=embed)

                user_pfp = (
                    message_user.avatar.url
                    if message_user.avatar
                    else message_user.default_avatar.url
                )

                embed = discord.Embed(
                    title="Edited Message",
                    description=f"**Before:** {edited_message['before_content']}\n**After:** {edited_message['after_content']}",
                    color=Colors.BASE_COLOR,
                )
                embed.set_author(name=message_user.display_name, icon_url=user_pfp)
                embed.set_footer(text=f"Page {index} of {len(sniped_messages)}")

                await ctx.send(embed=embed)
            else:
                return await ctx.warn(f"Invalid snipe index")
        else:
            return await ctx.deny(f"No edited messages to snipe")

    @commands.command(aliases=["cs"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def clearsnipe(self, ctx: commands.Context):
        channel_id = ctx.channel.id

        deleted_cache_exists = await self.bot.cache.get(
            f"deleted_messages_{channel_id}"
        )
        if deleted_cache_exists:
            await self.bot.cache.set(f"deleted_messages_{channel_id}", None)

        edited_cache_exists = await self.bot.cache.get(f"edited-{channel_id}")
        if edited_cache_exists:
            await self.bot.cache.set(f"edited-{channel_id}", None)

        if deleted_cache_exists or edited_cache_exists:
            await ctx.message.add_reaction(f"{Emojis.APPROVE}")
        else:
            await ctx.message.add_reaction(f"{Emojis.WARN}")

    @commands.command(
        name="afk", aliases=["away"], description="Let members know your AFK."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def afk(self, ctx: Context, *, status: str = None):

        if status is None:
            status = "AFK"

        current_time = int(datetime.datetime.now().timestamp())
        await self.bot.cache.set(f"afk-{ctx.author.id}", (status, current_time))

        return await ctx.approve(f"You're now **AFK**: **{status}**")

    TIKTOK_URL_PATTERN = re.compile(
        r"(https?://)?(www\.)?(vm\.tiktok\.com|t\.tiktok\.com|www\.tiktok\.com/@[A-Za-z0-9_.-]+/video|www\.tiktok\.com/t)/[A-Za-z0-9_/]+"
    )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        prefix = await self.bot.cache.get(f"prefix-{message.guild.id}") or ";"

        if message.content.strip().startswith(prefix + "afk"):
            return

        afk_data = await self.bot.cache.get(f"afk-{message.author.id}")
        if afk_data:
            status, start_time = afk_data
            start_time = datetime.datetime.fromtimestamp(start_time)
            now = datetime.datetime.now()
            time_away = humanize.naturaldelta(now - start_time)

            embed = discord.Embed(
                title=f"Welcome back {message.author.display_name}!",
                description=f"You were last seen **{time_away} ago.**",
                timestamp=datetime.datetime.now(),
            )
            embed.set_author(
                name=message.author.display_name, icon_url=message.author.avatar.url
            )
            await message.channel.send(embed=embed)
            await self.bot.cache.remove(f"afk-{message.author.id}")

        if message.mentions:
            for user in message.mentions:
                afk_data = await self.bot.cache.get(f"afk-{user.id}")
                if afk_data:
                    status, start_time = afk_data
                    start_time = datetime.datetime.fromtimestamp(start_time)
                    now = datetime.datetime.now()
                    time_away = humanize.naturaldelta(now - start_time)

                    embed = discord.Embed(
                        color=Colors.BASE_COLOR,
                        description=f"> 💤 {user.mention} is currently **AFK:** `{status}` - **{time_away} ago**",
                    )
                    await message.channel.send(embed=embed)

        if message.author == self.bot.user:
            return

        if message.content == self.bot.user.mention:
            guild_prefix = await self.bot.pool.fetchval(
                "SELECT prefix FROM guilds WHERE guild_id = $1", message.guild.id
            ) or (";")
            self_prefix = await self.bot.pool.fetchval(
                "SELECT prefix FROM selfprefix WHERE user_id = $1", message.author.id
            )
            if not self_prefix:
                embed = discord.Embed(
                    title="",
                    description=f"> Your **prefix** is: `{guild_prefix}`",
                    color=Colors.BASE_COLOR,
                )
                await message.channel.send(embed=embed)
            if self_prefix:
                embed = discord.Embed(
                    title="",
                    description=f"> Your **prefixes** are: `{self_prefix}` & `{guild_prefix}`",
                    color=Colors.BASE_COLOR,
                )
                await message.channel.send(embed=embed)

        # TIKTOK
        if message.content.lower().startswith("heal "):
            tiktok_link = message.content[5:].strip()
            if self.TIKTOK_URL_PATTERN.match(tiktok_link):
                api_url = f"https://tikwm.com/api/?url={tiktok_link}"

                async with aiohttp.ClientSession() as cs:
                    async with cs.get(api_url) as r:
                        data = await r.json()

                        video_url = data["data"]["play"]
                        likes = data["data"]["digg_count"]
                        comments = data["data"]["comment_count"]
                        shares = data["data"]["share_count"]
                        description = data["data"]["title"]
                        username = data["data"]["author"]["unique_id"]
                        avatar = data["data"]["author"]["avatar"]

                        async with cs.get(video_url) as video_response:
                            video_data = await video_response.read()

                            video_file = io.BytesIO(video_data)

                            await message.delete()

                            embed = discord.Embed(
                                description=f"{description}", color=Colors.BASE_COLOR
                            )
                            embed.set_footer(
                                text=f"❤️ {int(likes)} | 💬 {int(comments)} | 🔗 {int(shares)}"
                            )
                            embed.set_author(name=f"{username}", icon_url=avatar)

                            await message.channel.send(
                                file=discord.File(fp=video_file, filename="video.mp4"),
                                embed=embed,
                            )

    @group(
        name="selfprefix",
        description="Selfprefix settings.",
        invoke_without_command=True,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def selfprefix(self, ctx: Context):
        return await ctx.send_help(ctx.command)

    @selfprefix.command(
        name="set", aliases=["add", "use"], description="Set your selfprefix"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def selfprefix_set(self, ctx: Context, prefix: str) -> Message:

        if len(prefix) > 7:
            return await ctx.deny("Prefix is too long!")

        await self.bot.pool.execute(
            """
            INSERT INTO selfprefix (user_id, prefix)
            VALUES ($1, $2)
            ON CONFLICT (user_id)
            DO UPDATE SET prefix = $2
            """,
            ctx.author.id,
            prefix,
        )
        await self.bot.cache.set(f"selfprefix-{ctx.author.id}", prefix)
        return await ctx.approve(f"**Self Prefix** updated to `{prefix}`")

    @selfprefix.command(
        name="remove",
        aliases=["delete", "del", "clear"],
        description="Delete your selfprefix.",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def selfprefix_remove(self, ctx: Context):
        check = await self.bot.pool.fetchval(
            "SELECT * FROM selfprefix WHERE user_id = $1", ctx.author.id
        )
        if not check:
            return await ctx.deny(f"You dont have a **selfprefix** setup.")
        else:
            await self.bot.pool.execute(
                "DELETE FROM selfprefix WHERE user_id = $1", ctx.author.id
            )
            await self.bot.cache.remove(f"selfprefix-{ctx.author.id}")
            return await ctx.approve("Removed your **selfprefix**.")

    @hybrid_group(
        name="tiktok",
        aliases=["tt"],
        description="Tiktok commands",
        usage="tiktok <command>",
        invoke_without_command=True,
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tiktok(self, ctx: Context):
        await ctx.send_help(ctx.command)

    @tiktok.command(name="reposter", description="Repost a tiktok video")
    async def tiktok_reposter(self, ctx: Context, *, url: str):
        if self.TIKTOK_URL_PATTERN.match(url):
            api_url = f"https://tikwm.com/api/?url={url}"

            async with aiohttp.ClientSession() as cs:
                async with cs.get(api_url) as r:
                    data = await r.json()

                    video_url = data["data"]["play"]
                    likes = data["data"]["digg_count"]
                    comments = data["data"]["comment_count"]
                    shares = data["data"]["share_count"]
                    description = data["data"]["title"]
                    username = data["data"]["author"]["unique_id"]
                    avatar = data["data"]["author"]["avatar"]

                    if "images" in data["data"]:
                        images = data["data"]["images"]
                        embeds = self.create_slideshow_embeds(
                            description,
                            likes,
                            comments,
                            shares,
                            username,
                            avatar,
                            images,
                        )
                        await ctx.paginate(embeds)
                    else:
                        async with cs.get(video_url) as video_response:
                            video_data = await video_response.read()

                            video_file = io.BytesIO(video_data)
                            embed = discord.Embed(
                                description=f"{description}", color=Colors.BASE_COLOR
                            )
                            embed.set_footer(
                                text=f"❤️ {int(likes)} | 💬 {int(comments)} | 🔗 {int(shares)}"
                            )
                            embed.set_author(name=f"{username}", icon_url=avatar)

                            await ctx.send(
                                file=discord.File(fp=video_file, filename="video.mp4"),
                                embed=embed,
                            )

    def create_slideshow_embeds(
        self,
        description: str,
        likes: int,
        comments: int,
        shares: int,
        username: str,
        avatar: str,
        images: List[str],
    ) -> List[discord.Embed]:
        embeds = []
        for image_url in images:
            embed = discord.Embed(description=f"{description}", color=Colors.BASE_COLOR)
            embed.set_footer(
                text=f"❤️ {int(likes)} | 💬 {int(comments)} | 🔗 {int(shares)}"
            )
            embed.set_author(name=f"{username}", icon_url=avatar)
            embed.set_image(url=image_url)
            embeds.append(embed)
        return embeds

    @command(name="gif", description="Turns an image into a gif.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gif(self, ctx: Context):
        await ctx.typing()
        if ctx.message.reference:
            ref_message = await ctx.channel.fetch_message(
                ctx.message.reference.message_id
            )
            if ref_message.attachments:
                image_url = ref_message.attachments[0].url
            else:
                return await ctx.send(
                    "The replied-to message does not contain an image."
                )
        elif ctx.message.attachments:
            image_url = ctx.message.attachments[0].url
        else:
            try:
                image_url = ctx.message.content.split(" ")[1]
            except IndexError:
                return await ctx.send_help(ctx.command)

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    with io.BytesIO(image_data) as image_binary:
                        image = Image.open(image_binary)

                        # Convert the image to GIF
                        gif_buffer = io.BytesIO()
                        image.save(gif_buffer, format="GIF")
                        gif_buffer.seek(0)
                        await ctx.reply(
                            file=discord.File(gif_buffer, filename="output.gif")
                        )
                else:
                    await ctx.send("Failed to retrieve the image.")

    @hybrid_command(
        name="screenshot", aliases=["ss"], description="Screenshot a website."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def screenshot(self, ctx: Context, url: str, *, timeout: int = None):
        APIKEY = api.heal
        api_url = "http://localhost:1999/screenshot"

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        if timeout is None:
            timeout = 1

        params = {"url": url, "timeout": timeout}
        headers = {"api-key": APIKEY}

        async with ctx.typing():

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    api_url, params=params, headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()

                        screenshot_url = data.get("screenshot_url")

                        async with session.get(screenshot_url) as image_response:
                            if image_response.status == 200:
                                image_data = await image_response.read()

                                file = discord.File(
                                    io.BytesIO(image_data), filename="screenshot.png"
                                )

                                await ctx.send(file=file)
                            else:
                                await ctx.deny(
                                    "Failed to download screenshot image. Try again later."
                                )
                            if image_response.status == 403:
                                return await ctx.warn(f"{data['detail']}")

    @command(
        aliases=["createembed", "ce", "script"],
        description="Create an embed.",
    )
    @has_permissions(manage_messages=True)
    async def embed(self, ctx: Context, *, script: EmbedScript = None) -> Message:
        if script is None:
            return await ctx.neutral(
                f"Create embed code [**here**](https://healbot.lol/embed)"
            )
        return await ctx.send(**script)

    @command(name="firstmsg", description="Get the first message in the channel.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def firstmessage(self, ctx: Context):
        await ctx.typing()
        async for message in ctx.channel.history(limit=1, oldest_first=True):
            await ctx.reply(
                view=discord.ui.View().add_item(
                    discord.ui.Button(
                        style=discord.ButtonStyle.link,
                        label="first message",
                        url=message.jump_url,
                    )
                )
            )

    @commands.command(
        name="shazam", description="Get a track name from sound", aliases=["sh", "shzm"]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def shazam(self, ctx: Context):
        if ctx.message.reference:
            ref_message = await ctx.channel.fetch_message(
                ctx.message.reference.message_id
            )
            if ref_message.attachments:
                attachment = ref_message.attachments[0]
            else:
                await ctx.warn(
                    "The replied-to message does not contain a video or audio file."
                )
                return
        elif ctx.message.attachments:
            attachment = ctx.message.attachments[0]
        else:
            await ctx.warn("Please provide a video or audio file.")
            return
        if not (
            attachment.content_type.startswith("audio/")
            or attachment.content_type.startswith("video/")
        ):
            await ctx.warn("The provided file is not an audio or video file.")
            return

        msg = await ctx.neutral(
            f"> <:shazam:1273688697753047070> Searching for song..."
        )

        audio_data = await attachment.read()
        shazam = Shazam()

        try:
            song = await shazam.recognize(audio_data)
            if "track" not in song or "share" not in song["track"]:
                return await ctx.send("Could not recognize the track.")

            song_cover_url = song["track"]["images"].get("coverart", "")
            embed = discord.Embed(
                color=0x31333B,
                description=f"> <:shazam:1273688697753047070> **[{song['track']['share']['text']}]({song['track']['share']['href']})**",
            )
            embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar.url)
            if song_cover_url:
                embed.set_thumbnail(url=song_cover_url)
            await msg.edit(embed=embed)

        finally:
            if hasattr(shazam, "_session") and shazam._session:
                await shazam._session.close()

    @command(name="poll", aliases=["quickpoll", "qp"], description="Create a poll.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def poll(self, ctx: Context, *, question: str = None):
        await ctx.message.delete()
        emb = discord.Embed(description=question, color=Colors.BASE_COLOR)
        emb.set_author(name=f"{ctx.author.name}")
        message = await ctx.send(embed=emb)
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    @hybrid_command(
        name="removebg",
        aliases=["rembg", "transparent", "tp"],
        description="Removes a background from an image.",
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def removebg(self, ctx: Context, *, image: str = None):
        if ctx.message.attachments:
            image_url = ctx.message.attachments[0].url
        elif image:
            image_url = image
        else:
            return await ctx.warn("Please provide an image URL or upload an image.")

        await ctx.typing()

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status != 200:
                    return await ctx.warn("Failed to fetch the image.")
                image_data = await resp.read()

        try:
            input_image = BytesIO(image_data)
            input_image_bytes = input_image.getvalue()

            output_image_data = remove(input_image_bytes, force_return_bytes=True)

            output_image = BytesIO(output_image_data)
            output_image.seek(0)

            await ctx.reply(file=discord.File(fp=output_image, filename="output.png"))
        except Exception as e:
            await ctx.deny(f"Failed to remove background: {e}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):

        log_channel_id = 1278693282905329716
        log_channel = self.bot.get_channel(log_channel_id)

        if log_channel:
            embed = discord.Embed(
                title="Joined a New Guild",
                description=f"**Guild Name:** {guild.name}\n**Guild ID:** {guild.id}\n**Guild Owner:** {guild.owner} \n**User count:** {len(guild.members)}",
                color=Colors.APPROVE,
            )
            await log_channel.send(embed=embed)

    @hybrid_command(name="image", aliases=["img"], description="Search for an image.")
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def image(self, ctx: Context, *, query: str):
        APIKEY = api.heal
        api_url = "http://localhost:1999/browse/images"

        params = {"query": query, "safe_mode": "true"}
        headers = {"api-key": APIKEY}
        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    api_url, params=params, headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()

                        images = data.get("images", [])
                        if not images:
                            return await ctx.warn("No images found for your query.")

                        embeds = []
                        for image_data in images:
                            embed = discord.Embed(
                                title=f"Image result for: {query}",
                                color=Colors.BASE_COLOR,
                            )
                            embed.set_image(url=image_data["url"])
                            embed.set_footer(
                                text=f"Page {len(embeds) + 1} of {len(images)} | Safemode: True"
                            )
                            embeds.append(embed)

                        await ctx.paginate(embeds)
                    else:
                        await ctx.warn("Failed to retrieve images. Try again later.")

    @hybrid_command(name="google", aliases=["search"], description="Search online.")
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def google(self, ctx: Context, *, query: str):
        APIKEY = api.heal
        api_url = "http://localhost:1999/browse/search"

        params = {"query": query}
        headers = {"api-key": APIKEY}

        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    api_url, params=params, headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()

                        results = data.get("results", [])
                        if not results:
                            return await ctx.warn("No results found for your query.")

                        embeds = []
                        for result_data in results:
                            title = result_data.get("title", "No title")
                            url = result_data.get("url", "No URL")
                            snippet = result_data.get(
                                "description", "No description available"
                            )
                            image = result_data.get("image")

                            embed = discord.Embed(
                                title=f"{title}",
                                url=url,
                                description=f"{snippet}",
                                color=Colors.BASE_COLOR,
                            )
                            embed.set_footer(
                                text=f"Page {len(embeds) + 1} of {len(results)}"
                            )
                            embed.set_thumbnail(url=image)
                            embeds.append(embed)

                        await ctx.paginate(embeds)
                    else:
                        await ctx.warn("Failed to retrieve results. Try again later.")

    @commands.command(
        name="selfpurge",
        aliases=["spurge", "me"],
        description="Clears your own messages.",
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def selfpurge(self, ctx: Context, amount: int = 100):
        deleted = await ctx.channel.purge(
            limit=amount, check=lambda m: m.author == ctx.author
        )

    @commands.command(
        name="botclear",
        aliases=["bc"],
        description="Clears messages sent by bots in the channel.",
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def botclear(self, ctx: Context, amount: int = 100):
        deleted = await ctx.channel.purge(limit=amount, check=lambda m: m.author.bot)
        await ctx.message.add_reaction(f"<:approve:1276192812127359081>")

    @hybrid_group(
        name = "timezone",
        aliases = ["tz"],
        description = "View your current time or somebody elses.",
        invoke_without_command = True
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def timezone(self, ctx: Context, *, user: discord.Member = None):
        if user is None:
            user = ctx.author
        user_data = await self.bot.pool.fetchrow("SELECT timezone FROM timezones WHERE user_id = $1", user.id)
        if user_data is None:
                return await ctx.warn(f"You have not set your timezone yet. Use `{ctx.prefix}timezone set <timezone>` to set it.")
        timezone = user_data['timezone']
        tz = pytz.timezone(timezone)
        current_time = datetime.datetime.now(tz)
        formatted_time = current_time.strftime('%I:%M %p')

        if user is ctx.author:
            return await ctx.neutral(f"{ctx.author.mention}: Your local time is: **{formatted_time}**. ")
        else:
            return await ctx.neutral(f"{ctx.author.mention}: {user.mention}'s local time is **{formatted_time}**.")
                
        
    @timezone.command(
        name = "set",
        description = "Set your timezone."
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def timezone_set(self, ctx: Context, *, timezone: str = None):
        timezone = timezone.capitalize()
        if timezone not in TIMEZONEMAPPING:
            return await ctx.warn(f"The **timezone** `{timezone}` is not a valid timezone.")
        if timezone in TIMEZONEMAPPING:
            timezone = TIMEZONEMAPPING[timezone]

        await self.bot.pool.execute("INSERT INTO timezones (user_id, timezone) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET timezone = $2", ctx.author.id, timezone)
        return await ctx.approve(f"Set your timezone to `{timezone}`.")

    @timezone.command(
        name = "view",
        description = "View yours or somebody elses timezone."
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def timezone_view(self, ctx: Context, *, user: Union[discord.Member, discord.User] = None):
        if user is None:
            user = ctx.author
        user_data = await self.bot.pool.fetchrow("SELECT timezone FROM timezones WHERE user_id = $1", user.id)
        if user_data is None:
                return await ctx.warn(f"You have not set your timezone yet. Use `{ctx.prefix}timezone set <timezone>` to set it.")
        timezone = user_data['timezone']
        tz = pytz.timezone(timezone)
        current_time = datetime.datetime.now(tz)
        formatted_time = current_time.strftime('%I:%M %p')

        if user is ctx.author:
            return await ctx.neutral(f"{ctx.author.mention}: Your local time is: **{formatted_time}**. ")
        else:
            return await ctx.neutral(f"{ctx.author.mention}: {user.mention}'s local time is **{formatted_time}**.")


async def setup(bot: Heal):
    await bot.add_cog(Utility(bot))
