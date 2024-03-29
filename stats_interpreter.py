
#Interprets html to txt formatting to get the stats we want
#Everything below will return an integer/float except for the date, link and timestring, which return a string

class jstris_stats:

    def username(usernamestring):
        # format
        # streasure</a>
        endindex = usernamestring.index("</a>")
        usernamestring = usernamestring[ : endindex]
        return usernamestring

    # jstris time format to seconds
    def jstris_time(timestring):

        # example time format in the file
        # <td><strong>1:47.<span class="time-mil">171</span></strong></td>

        # example without any milliseconds
        # <td><strong>3:27</strong></td>

        # example without minutes
        # <td><strong>2.798</strong></td>

        # Use this because somethings there is a space before <td><strong> for no apparent reason
        timestringbeginning = timestring.index("<td><strong>")

        # check for minutes with the colon
        if ":" in timestring:
            minutesbeg = timestringbeginning + 12
            minutesend = timestring.index(":")
            minutes = timestring[minutesbeg: minutesend]
            hasminutes = True
        else:
            minutes = "0"
            hasminutes = False

        # check for milliseconds with '.'
        # time-mil only shows up if there are minutes

        if "." in timestring and hasminutes == True:
            millisecondsbeg = timestring.index("time-mil") + 10
            millisecondsend = timestring.rindex("</span></strong></td>")
            milliseconds = timestring[millisecondsbeg: millisecondsend]
            while len(milliseconds) < 3:
                milliseconds += "0"
            hasmilliseconds = True
        elif "." in timestring and hasminutes == False:
            millisecondsbeg = timestring.index(".") + 1
            millisecondsend = timestring.rindex("</strong></td>")
            milliseconds = timestring[millisecondsbeg: millisecondsend]
            while len(milliseconds) < 3:
                milliseconds += "0"
            hasmilliseconds = True
        else:
            milliseconds = "0"
            hasmilliseconds = False

        # Guaranteed to have seconds
        # index where seconds begins and ends depends whether there are minutes and milliseconds

        if hasminutes == True:
            secondsbegin = timestring.index(":") + 1
        else:
            secondsbegin = timestringbeginning + 12
        if hasmilliseconds == True:
            secondsend = timestring.index(".")
        else:
            secondsend = timestring.rindex("</strong></td>")

        seconds = timestring[secondsbegin: secondsend]

        return (60 * int(minutes) + int(seconds) + 0.001 * int(milliseconds))


    # seconds to clock format
    def seconds_to_clock(timefloat):
        minutes = int(timefloat // 60)
        seconds = int(timefloat - 60 * minutes // 1)
        milliseconds = round(timefloat - (60 * minutes) - seconds, 3)

        minutes = str(minutes)
        # deals with seconds when it's below 10 like 1:06
        if seconds < 10:
            seconds = "0" + str(seconds)
        else:
            seconds = str(seconds)
        milliseconds = str(milliseconds)

        timestring = minutes + ":" + seconds + "." + milliseconds[2:]
        return timestring

    # clock to seconds format
    def clock_to_seconds(timestring):
        # format
        # 1:43.365

        colonindex = timestring.index(":")
        periodindex = timestring.index(".")
        minutes = int(timestring[: colonindex])
        seconds = int(timestring[colonindex + 1: periodindex])
        milliseconds = float(timestring[periodindex:])

        return round(60 * minutes + seconds + milliseconds, 3)

    def blocks(blocksstring):
        # example line
        # <td>236</td>

        blockstringend = blocksstring.rindex("</td>")
        blocksstring = int(blocksstring[4:blockstringend])
        return blocksstring

    def pps(ppsstring):
        # example line
        # <td>0.08</td>

        ppsstringend = ppsstring.rindex("</td>")
        ppsstring = float(ppsstring[4:ppsstringend])
        ppsstring = round(ppsstring, 2)
        return ppsstring

    def finesse(finessestring):
        # example line
        # <td>48</td>

        finessestringend = finessestring.rindex("</td>")
        finessestring = int(finessestring[4:finessestringend])
        return finessestring

    def date(datestring):
        # example
        # <td>2020-08-11 18:06:53</td>

        datestringend = datestring.rindex("</td>")
        datestring = datestring[4:datestringend]
        return datestring

    def link(linkstring):
        # example
        # <a href="https://jstris.jezevec10.com/replay/19483494" target="_blank">(V3)<img src="https://jstris.jezevec10.com/res/play.png"></a>

        if "https://jstris.jezevec10.com/replay/" in linkstring:
            linkstringend = linkstring.index("target") - 2
            linkstring = linkstring[9:linkstringend]
        else:
            linkstring = "-"
        return linkstring

    def jstris_score(scorestring):
        # example
        # <td><strong>174,325</strong></td>

        scorestring = scorestring[scorestring.index("<td><strong>") + 12: scorestring.rindex("</strong></td>")]
        scorestring = scorestring.replace(",", "")

        return scorestring

    def ppb(ppbstring):
        # example
        # <td>379.15</td>

        ppbstringend = ppbstring.rindex("</td>")
        ppbstring = float(ppbstring[4:ppbstringend])
        ppbstring = round(ppbstring, 2)
        return ppbstring



# Deals with all my formatting nonsense in unorderedstats.txt
# Does not support ultra runs and other stuff yet

class my_stats:

    def unordered_username(statstring):
        # format:
        # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720

        usernameindex = 0
        timeindex = statstring.index("Time: ")
        final_username = statstring[usernameindex: timeindex - 2]

        return final_username

    def unordered_time(statstring):
        # format:
        # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720

        timeindex = statstring.index("Time: ")
        blocksindex = statstring.index("Blocks: ")
        final_time = statstring[timeindex + 6: blocksindex - 2]

        return final_time

    def unordered_block(statstring):
        # format:
        # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720

        blocksindex = statstring.index("Blocks: ")
        ppsindex = statstring.index("PPS: ")
        final_block = int(statstring[blocksindex + 8: ppsindex - 2])

        return final_block

    def unordered_pps(statstring):
        # format:
        # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720

        ppsindex = statstring.index("PPS: ")
        finesseindex = statstring.index("Finesse: ")
        final_pps = float(statstring[ppsindex + 5: finesseindex - 2])

        return final_pps

    def unordered_finesse(statstring):
        # format:
        # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720

        finesseindex = statstring.index("Finesse: ")
        dateindex = statstring.index("Date: ")
        final_finesse = int(statstring[finesseindex + 9: dateindex - 2])

        return final_finesse

    def unordered_date(statstring):
        # format:
        # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720

        dateindex = statstring.index("Date: ")
        linkindex = statstring.index("Link: ")
        final_date = statstring[dateindex + 6: linkindex - 2]

        return final_date

    def unordered_link(statstring):
        # format:
        # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720

        linkindex = statstring.index("Link: ")
        final_link = statstring[linkindex + 6: ]

        return final_link

    def unordered_clock_to_seconds(timestring):
        return jstris_stats.clock_to_seconds(my_stats.unordered_time(timestring))

    def statsstring_to_tuple(statsstring):
        # format
        # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720
        return (my_stats.unordered_username(statsstring),
                my_stats.unordered_time(statsstring),
                my_stats.unordered_block(statsstring),
                my_stats.unordered_pps(statsstring),
                my_stats.unordered_finesse(statsstring),
                my_stats.unordered_date(statsstring),
                my_stats.unordered_link(statsstring))

    def tuple_to_statsstring(t):
        time = t[1]
        try:
            time = jstris_stats.seconds_to_clock(t[1])
        except:
            pass
        return "{}  Time: {}  Blocks: {}  PPS: {}  Finesse: {}  Date: {}  Link: {} \n".format(  t[0], time, t[2], t[3],
                                                                                             t[4], t[5], t[6])
