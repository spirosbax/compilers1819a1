"""
Sample script to test ad-hoc scanning by table drive.
This accepts a number with optional decimal part [0-9]+(\.[0-9]+)?

NOTE: suitable for optional matches
"""

def getchar(text,pos):
    """ returns char category at position `pos` of `text`,
    or None if out of bounds """
    if pos<0 or pos>=len(text): return None
    c = text[pos]

    # **Σημείο #3**: Προαιρετικά, προσθέστε τις δικές σας ομαδοποιήσεις
    if c=='0': return 'D0'  # 0 grouped together
    if c>='0' and c<='2': return 'D02'  # 0..2 grouped together
    if c=='3': return 'D3'  # 3 grouped together
    if c>='0' and c<='4': return 'D04'  # 0..4 grouped together
    if c=='5': return 'D5'  # 5 grouped together
    if c>='0' and c<='9': return 'D09' # 0..9 grouped together
    return c  # anything else


def scan(text,transitions,accepts):
    """ scans `text` while transitions exist in
    'transitions'. After that, if in a state belonging to
    `accepts`, it returns the corresponding token, else ERROR_TOKEN.
    """

    # initial state
    pos = 0
    state = 's0'
    # memory for last seen accepting states
    last_token = None
    last_pos = None

    while True:
        c = getchar(text,pos)	# get next char (category)
        if state in transitions and c in transitions[state]:
            state = transitions[state][c]	# set new state
            pos += 1	# advance to next char
            # remember if current state is accepting
            if state in accepts:
                last_token = accepts[state]
                last_pos = pos
        else:   # no transition found
            if last_token is not None:	# if an accepting state already met
                return last_token,last_pos
            # else, no accepting state met yet
            return 'ERROR_TOKEN',pos


# **Σημείο #1**: Αντικαταστήστε με το δικό σας λεξικό μεταβάσεων
transitions = { 's0': { 'D0':'s1','D02':'s1','D3':'s2' },
                's1': { 'D0':'s3','D02':'s3','D3':'s3','D04':'s3','D5':'s3','D09':'s3' },
                's2': { 'D0':'s3','D02':'s3','D3':'s3','D04':'s3','D5':'s3.1' },
                's3': { 'D0':'s4','D02':'s4','D3':'s4','D04':'s4','D5':'s4','D09':'s4' },
                's3.1': { 'D0':'s4' },
                's4': { 'D0':'s5','D02':'s5','D3':'s5','D04':'s5','D5':'s5','D09':'s5' },
                's5': { 'D0':'s6','D02':'s6','D3':'s6','D04':'s6','D5':'s6','D09':'s6' },
                's6': { 'M':'s9','G':'s11','K':'s7' },
                's9': { 'P':'s10' },
                's10':{ 'S':'s8f' },
                's7': { 'T':'s8f' },
                's11':{ 'D0':'s12','D02':'s12','D3':'s12','D04':'s12','D5':'s12','D09':'s12' },
                's12':{ 'D0':'s6','D02':'s6','D3':'s6','D04':'s6','D5':'s6','D09':'s6' }
              }

# **Σημείο #2**: Αντικαταστήστε με το δικό σας λεξικό καταστάσεων αποδοχής
accepts = { 's8f':'WIND_TOKEN' }


# get a string from input
text = input('give some input>')

# scan text until no more input
while text:		# i.e. len(text)>0
    # get next token and position after last char recognized
    token,pos = scan(text,transitions,accepts)
    if token=='ERROR_TOKEN':
            print('unrecognized input at position',pos,'of',text)
            break
    print("token:",token,"text:",text[:pos])
    # new text for next scan
    text = text[pos:]

