SCRIPT_SRC = '''
WORKLOG=$HOME/worklog.md

worklog() {
    theDate=`date +'%d %b %Y'`
    if ! grep --quiet "$theDate" $WORKLOG
    then
        echo '' >> $WORKLOG
        echo \#\# $theDate >> $WORKLOG
        echo '- Start @ ' >> $WORKLOG
        echo '- Lunch ' >> $WORKLOG
        echo '- Stop @ ' >> $WORKLOG
    fi

    $VISUAL '+normal GA' $WORKLOG
}

alias wl=worklog
'''

def run():
    print(SCRIPT_SRC)

if __name__ == '__main__':
    run()
