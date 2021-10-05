
#Interprets html to txt formatting to get the stats we want
#Everything below will return an integer/float except for the date, link and timestring, which return a string

#jstris time format to seconds
def jstris_time(timestring):

    # example time format in the file
    # <td><strong>1:47.<span class="time-mil">171</span></strong></td>

    # example without any milliseconds
    # <td><strong>3:27</strong></td>

    # example without minutes
    # <td><strong>2.798</strong></td>


    #Use this because somethings there is a space before <td><strong> for no apparent reason
    timestringbeginning = timestring.index("<td><strong>")

    # check for minutes with the colon
    if ":" in timestring:
        minutesbeg = timestringbeginning + 12
        minutesend = timestring.index(":")
        minutes = timestring[minutesbeg : minutesend]
        hasminutes = True
    else:
        minutes = "0"
        hasminutes = False

    # check for milliseconds with '.'
    # time-mil only shows up if there are minutes

    if "." in timestring and hasminutes == True:
        millisecondsbeg = timestring.index("time-mil") + 10
        millisecondsend = timestring.rindex("</span></strong></td>")
        milliseconds = timestring[millisecondsbeg : millisecondsend]
        hasmilliseconds = True
    elif "." in timestring and hasminutes == False:
        millisecondsbeg = timestring.index(".") + 1
        millisecondsend = timestring.rindex("</strong></td>")
        milliseconds = timestring[millisecondsbeg : millisecondsend]
        hasmilliseconds = True
    else:
        milliseconds = "0"
        hasmilliseconds = False

    # Guaranteed to have seconds
    # index where seconds begins and ends depends whether there are minutes and milliseconds

    if hasminutes == True:
        secondsbegin =  timestring.index(":") + 1
    else:
        secondsbegin = timestringbeginning + 12
    if hasmilliseconds == True:
        secondsend = timestring.index(".")
    else:
        secondsend = timestring.rindex("</strong></td>")

    seconds = timestring[secondsbegin : secondsend]


    return (60 * int(minutes) + int(seconds) + 0.001 * int(milliseconds))

#seconds to clock format
def time_reverse(timefloat):
    minutes = int(timefloat // 60)
    seconds = int(timefloat - 60 * minutes // 1)
    milliseconds = round(timefloat - (60 * minutes) - seconds,3)

    minutes = str(minutes)
    #deals with seconds when it's below 10 like 1:06
    if seconds < 10:
        seconds = "0" + str(seconds)
    else:
        seconds = str(seconds)
    milliseconds = str(milliseconds)

    timestring = minutes + ":" + seconds + "." + milliseconds[2:]
    return timestring

#clock to seconds format
def clock_to_seconds(timestring):
    # format
    # 1:43.365

    colonindex = timestring.index(":")
    periodindex = timestring.index(".")
    minutes = int(timestring[ : colonindex])
    seconds = int(timestring[ colonindex + 1: periodindex])
    milliseconds = float(timestring[ periodindex : ])

    print(timestring, minutes, seconds, milliseconds)

    return round(60 * minutes + seconds + milliseconds, 3)

def blocks(blocksstring):
    #example line
    #<td>236</td>
    if blocksstring[0] == " ":
        blocksstring = blocksstring[1:]
    blockstringend = blocksstring.rindex("</td>")
    blocksstring = int(blocksstring[4:blockstringend])
    return blocksstring

def pps(ppsstring):
    #example line
    #<td>0.08</td>
    if ppsstring[0] == " ":
        ppsstring = ppsstring[1:]
    ppsstringend = ppsstring.rindex("</td>")
    ppsstring = float(ppsstring[4:ppsstringend])
    ppsstring = round(ppsstring,2)
    return ppsstring

def finesse(finessestring):
    # example line
    # <td>48</td>
    if finessestring[0] == " ":
        finessestring = finessestring[1:]
    finessestringend = finessestring.rindex("</td>")
    finessestring = int(finessestring[4:finessestringend])
    return finessestring

def date(datestring):
    #example
    #<td>2020-08-11 18:06:53</td>
    if datestring[0] == " ":
        datestring = datestring[1:]
    datestringend = datestring.rindex("</td>")
    datestring = datestring[4:datestringend]
    return datestring

def link(linkstring):
    #example
    #<a href="https://jstris.jezevec10.com/replay/19483494" target="_blank">(V3)<img src="https://jstris.jezevec10.com/res/play.png"></a>
    if "https://jstris.jezevec10.com/replay/" in linkstring:
        linkstringend = linkstring.index("target") - 2
        linkstring = linkstring[9:linkstringend]
    else:
        linkstring = "-"
    return linkstring


