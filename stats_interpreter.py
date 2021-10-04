
#Interprets html to txt formatting to get the stats we want
#Everything below will return an integer/float except for the date, link and timestring, which return a string

#clock format to seconds
def time(timestring):
    # example time thing in the file
    # <td><strong>1:47.<span class="time-mil">171</span></strong></td>
    # example without any milliseconds
    # <td><strong>3:27</strong></td>

    timestringbeginning = timestring.index("<td><strong>")
    timestringcolon = timestring.index(":")

    minutes = timestring[timestringbeginning + 12: timestringcolon]

    if len(timestring) > 35:
        timestringperiod = timestring.index('.')
        timestringms = timestring.index("time-mil")
        seconds = timestring[timestringcolon + 1: timestringperiod]
        milliseconds = timestring[timestringms + 10: timestringms + 13]
    else:
        # accounts for case without ms
        seconds = timestring[timestringcolon + 1: -15]
        milliseconds = 0

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


