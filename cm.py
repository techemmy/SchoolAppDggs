# CONTENT MANAGEMENT FILE
def Content():
    """ This function provides live data to the server
        DATA including: images in GALLARY,
                        subjects and percentages in RESULTS,
                        alumni in ALUMNI
    """
    CONT = {"Imgs": ["g4.jpg", "g3.jpg","g5.jpg","a.jpg", "a2.jpg", "g8.jpg"],
            "Res": [['Mathematics', 85],['English Language', 80],
                    ['Civic Education', 90],['Physics', 80],
                    ['Financial Accounting', 85],['Literature-in-English', 79],
                    ['Chemistry', 82],['Commerce', 89],['C.R.S', 86],
                    ['Geography', 91],['Yoruba', 79],
                    ['Agricultural Science', 89], ['Computer Science', 93],
                    ['Animal Husbandry', 91], ['Further Mathematics', 79],
                    ['Data Processing', 96],
                    ],
            "Term-Dates": [
                    ['mid-term-break', '7th Week of the term'],
                    ['Valendictory Service', '1st Saturday in August'],
                    ['Carol Party', 'Friday 2nd Week in December'],
                    ['1st Term Vacation', 'Friday 2nd Week in September'],
                    ],
            "Alumni": [['Leander danuel', '2019/2020'],
                       ['Stony danuel', '2019/2020'],
                       ['Duels Linky', '2019/2020'],
                       ['Olageshin Jesujinde', '2019/2020'],
                       ['Emmanuel Leander', '2019/2020'],
                       ['Joshua Linda', '2019/2020'],
                       ['Adebayo David', '2019,2020'],
                       ['Adebayo Emmanuel', '2019/2020'],
                      ]
            }
    return CONT