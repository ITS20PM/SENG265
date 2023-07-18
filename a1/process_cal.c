#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#define MAX_LINE_LEN 200
#define MAX_EVENTS 1000

/*
    Function: validInput
    Description: check if the input from the console is valid
    Inputs:
        - argc: the number of inputted parameters from the console
    Outputs:
        - None
*/
void validInput(int argc){
    if(argc < 3){
        printf("invalid input\n");
        exit(1);    
    }
}

/*
    Function: generateInput
    Description: convert input from the console into (year/month/day) format
    Inputs: 
        - end: the proper forrmat of the inputted calendar date
        - start: the inputted calendar date from the console 
    Outputs:
        - None
*/
void generateInput(char *end, char *start){
    int begin = 0;
    for(int i = 0; i < strlen(start); i++){
        if(start[i]=='='){
            begin = i+1;
            break;
        }
    }
    
    for(int i = 0; i < strlen(start)-begin; i++){
        end[i] = start[i+begin];
    }
    end[strlen(start)-begin] ='\0';
}

/*
    Function: findLeftPos
    Description: find the position of the leftmost '>'
    Inputs:
        - line: each line of event data from the xml file
    Outputs: return position of the leftmost '>' as integer
        - pos: position of the leftmost '>'
*/
int findLeftPos(char *line){
    int res = 0;
    for(int i = 0; i < strlen(line)-2; i++){
        if(line[i]=='>'){
            res = i+1;
            break;
        }
    }
    return res;
}

/*
    Function: findRightPos
    Description: find the position of the rightmost '<'
    Inputs:
        - line: each line of event data from the xml file
    Outputs: return position of the rightmost '<' as integer
        - pos: position of the rightmost '<'
*/
int findRightPos(char *line){
    int res = 0;
    for(int j = strlen(line)-3; j >= 0; j--){
        if(line[j]=='<'){
            res = j-1;
            break;
        }
    }
    return res;
}

//generate data from the xml file
/*
    Function: generateData
    Description: generate data of every event from the xml file
    Inputs:
        - info: trying to store information from the data in the xml file per line
        - line: each line of event data from the xml file
    Outputs:
        - None
*/
void generateData(char *info, char *line){
    int left = 0, right = 0, start = 0;
    
    left = findLeftPos(line);//find the first position right after '>' 
    right = findRightPos(line);//find the rightmost position of '<'

    while(start <= right-left){
        info[start] = line[left+start];
        start++;
    }
    info[start] ='\0';
}

/*
    Function: convertDate
    Description: convert input date from the event into integer
    Inputs:
        - cur: current input date from the event
    Outputs: return the date from the event as an integer
        - res: date from the event as an integer form
*/
int convertDate(char *cur){
    int res = 0, base = 1;
    for(int i = strlen(cur)-1; i >= 0; i--){
        int digit = cur[i]-'0';
        res += base*digit;
        base *= 10;
    }
    return res;
}

/*
    Function: convertYr
    Description: transform inputted date (year/month/date) into year
    Inputs:
        - time: the calendar date inputted from the console
    Outputs: return the year in integer
        - res: the year of the inputted calendar date
*/
int convertYr(char *time){
    int res = 0, i = 0, base = 1;
    while(i < strlen(time) && time[i]!='/'){
        i++;
    }
    for(int j = i-1; j >= 0; j--){
        int digit = time[j]-'0';
        res += base*digit;
        base *= 10;
    }
    return res;
}

/*
    Function: convertDay
    Description: transform inputted date (year/month/date) into day
    Inputs:
        - time: the calendar date inputted from the console
    Outputs: return the day in integer
        - res: the day of the inputted calendar date
*/
int convertDay(char *time){
    int res = 0, i = (int)(strlen(time)-1), base = 1;
    while(i >= 0 && time[i]!='/'){
        int digit = time[i]-'0';
        res += digit*base;
        base *= 10;
        i--;
    }
    return res;
}

/*
    Function: convertMth
    Description: transform inputted date (year/month/date) into month
    Inputs: 
        - time: the date inputted from the console
    Outputs: return the month in integer
        - res: the month of the inputted calendar date
*/
int convertMth(char *time){
    int left = 0, right = (int)(strlen(time)-1), res = 0, base = 1;
    for(int i = right; i >= 0; i--){
        if(time[i]=='/'){
            right = i-1;
            break;
        }
    }
    for(int i = 0; i < strlen(time); i++){
        if(time[i]=='/'){
            left = i+1;
            break;
        }
    }
    while(right>=left){
        int digit = time[right]-'0';
        res += base*digit;
        base *= 10;
        right--;
    }
    return res;
}

/*
    Function: length
    Description: compute the length of the integer
    Inputs:
        - num: integer to be used to find its length
    Outputs: return the length of the num as integer
        - res: length of the num
*/
int length(int num){
    int res = 0, n = num;
    while(n!=0){
        n /= 10;
        res++;
    }
    return res;
}

/*
    Function: createcalendarDate
    Description: generate calendar date as a decimal format
    Inputs: 
        - day: day of the current event
        - month: month of the current event
        - year: year of the current event
    Outputs: return calendar date as an integer (year+month+day) format
*/
int createCalendarDate(int day, int month, int year){
    int time = 0, base = 1;
    
    while(base <= day){
        base *= 10;
    }
    time += day;
    if(length(day)==1){
        base *= 10;
    }
    time += (base*month);

    base = 1;
    while(base <= time){
        base *= 10;
    }
    if(length(month)==1){
        base *= 10;
    }
    time += (base*year);
    return time;
}

/*
    Function: validEvent
    Description: check if the current event is valid
    Inputs:
        - event: event array that stores each event from the xml file
        - startDate: startDate range from the console used for looking for valid event
        - endDate: endDate range from the console used for looking for valid event
        - i: current index of the current event to be evaluted
    Outputs: return the integer for validity
        - 1: current calendar date is in the event
        - 0: current calendar date is not in the event
*/
int validEvent(char event[][MAX_LINE_LEN], char *startDate, char *endDate, int i){
    int day, month, year, time1, time2;
    int day2, month2, year2;
    day = convertDate(event[i+3]);
    month = convertDate(event[i+4]);
    year = convertDate(event[i+5]);

    time1 = createCalendarDate(day, month, year);

    day2 = convertDay(startDate);
    month2 = convertMth(startDate);
    year2 = convertYr(startDate);
    if(time1 < createCalendarDate(day2, month2, year2)){
        return 0;
    }

    day2 = convertDay(endDate);
    month2 = convertMth(endDate);
    year2 = convertYr(endDate);
    if(time1 > createCalendarDate(day2, month2, year2)){
        return 0;
    }

    return 1;
}

/*
    Function: storeEvent
    Description: store valid events into output array
    Inputs:
        - event: event array that stores all the event from the xml file
        - output: array that stores valid event's data to be printed to the screen
        - curIndex: current index of the current valid event 
        - count: current index to store the current valid event into output array
    Outputs:
        - None
*/
void storeEvent(char event[][MAX_LINE_LEN], char output[][MAX_LINE_LEN], int curIndex, int count){
    for(int i = 0; i < 9; i++){
        strcpy(output[count+i], event[curIndex+i]);
    }
}

/*
    Function: findEvent
    Description: find the valid event from the event array within the input range
    Inputs:
        - event: event array that stores all the event from the xml file
        - output: array that stores valid event's data to be printed to the screen
        - startDate: startDate range from the console used for looking for valid event
        - endDate: endDate range from the console used for looking for valid event
    Outputs:
        - None
*/
void findEvent(char event[][MAX_LINE_LEN], char output[][MAX_LINE_LEN], char *startDate, char *endDate){
    int count = 0; //keeps track of the size of the array
    for(int i = 0; i < 1000 && (int)(strlen(event[i])>0); i+=9){
        if(validEvent(event, startDate, endDate, i)==1){
            storeEvent(event, output, i, count);
            count += 9;
        }
    }
}

/*
    Function: formatTime
    Description: format each specific time as decimal number
    Inputs:
        - time: the time of the event
    Outputs: return the time of the event in decimal form
*/
int formatTime(char *time){
    int i = (int)(strlen(time)-1), base = 1, res = 0;
    while(i >= 0){
        if(time[i]!=':'){
            int digit = time[i]-'0';
            res += digit*base;
            base *= 10;
        }
        i--;
    }
    return res;
}

/*
    Function: formatOutput
    Description: print the time of each event
    Inputs:
        - time: current time to be formatted according to the instruction
    Outputs:
        - None
*/
void formatOutput(int time){
    if((time/100)%12 > 0 && (time/100)%12 <10)
        printf("0");

    if((time/100)>12){//check if its in the afternoon
        printf("%d", (time/100)%12);
    }else if(time<100){//check if its 12 in the midnight (convert to 12:xx am)
        printf("%d", 12);
    }else{
        printf("%d", time/100);
    }
    printf(":");
    if(time%100<10)
        printf("0");

    printf("%d ", time%100);
    if((time/100)>=12){
        printf("PM");
    }else{
        printf("AM");
    }
}

/*
    Function: printEvent
    Description: strcture the output for each event information
    Inputs:
        - output: array that stores valid event's data to be printed to the screen
        - begin: beginning index of the current event of the current day
        - startTime: starting time of the event
        - endTime: ending time of the event 
    Outputs:
        - None
*/
void printEvent(char output[][MAX_LINE_LEN], int begin, int startTime, int endTime){
    printf("\n");
    formatOutput(startTime);
    printf(" to ");
    formatOutput(endTime);
    printf(": %s ", output[begin]);
    printf("{{%s}} | %s", output[begin+2], output[begin+1]);
}

/*
    Function: ValidTime
    Description: check if the current time of the current day is valid
    Inputs:
        - output: array that stores valid event's data to be printed to the screen
        - targetTime: current time of the current day to be searched of
        - targetDay: current day of the current day
    Outputs: return the integer value that indicates wheter the current time of the day is valid
        - 1: the current time of the current day is valid 
        - 0: the current time of the current day is invalid
*/
int ValidTime(char output[][MAX_LINE_LEN], int targetTime, int targetDay){
    int curDay;
    for(int i = 0; i < MAX_EVENTS&&strlen(output[i])>0; i+=9){
        if(formatTime(output[i+7])==targetTime){
            curDay = createCalendarDate(convertDay(output[i+3]), convertMth(output[i+4]), convertYr(output[i+5]));
            if(curDay == targetDay){
                return 1;
            }
        }
    }
    return 0;
}

/*
    Function: searchDate
    Description: search for the position of the targetted time of the day
    Inputs:
        - output: array that stores valid event's data to be printed to the screen
        - targetTime: the current time of the day to be searched of
        - targerDate: the current target calendar date
    Outputs: integer is used to return the position of the targetted time 
        - 0: the targetted time of the day has not been found
        - i+7: the correct position of the targetted time if it is found 
*/
int searchDate(char output[][MAX_LINE_LEN], int targetTime, int targetDate){
    int curDate;
    for(int i = 0; i < MAX_EVENTS && strlen(output[i])>0; i += 9){
        curDate = createCalendarDate(convertDay(output[i+3]), convertMth(output[i+4]), convertYr(output[i+5]));
        if(curDate==targetDate){
            if(formatTime(output[i+7])==targetTime){
                return i+7;
            }
        }
    }
    return 0;
}

/*
    Function: ValidDate
    Description: Check if the target Date is valid
    Inputs:
        - output: array that stores valid event's data to be printed to the screen
        - targetDate: the current date to be searched of
    Outputs: integer used to check if the date is valid or not
        - 1: the inputted target date is valid
        - 0: the inputted target date is invalid
*/
int ValidDate(char output[][MAX_LINE_LEN], int targetDate){
    int curDate;
    for(int i = 0; i < MAX_EVENTS && strlen(output[i])>0; i += 9){
        curDate = createCalendarDate(convertDay(output[i+3]), convertMth(output[i+4]), convertYr(output[i+5]));
        if(targetDate == curDate){
            return 1;
        }
    }
    return 0;
}

/*
    Function: formatEvent
    Description: format each valid event according according to the expected output in the text file
    Inputs: 
        - output: array that stores valid event's data to be printed to the screen
        - calendarDate: the calendar date (in integer form) as: year+month+day
        - curIndex: the current index of the event
    Outputs:
        - None
*/
void formatEvent(char output[][MAX_LINE_LEN], int calendarDate, int curIndex){
    //go over through each time of a day
    int beginTime = 0, endTime = 0;
    int k = 0;
    while(k <= 2359){
        if(ValidTime(output, k, calendarDate)==1){
            beginTime = k; // convert to current start-time in (12:34) format

            curIndex = searchDate(output, k, calendarDate);
            endTime = formatTime(output[curIndex+1]); //convert to current endtime
            printEvent(output, curIndex-7, beginTime, endTime);
        }
    
        if(k%100>=59){
            k += 40;
        }
        k += 1;
    }
    
}

/*
    Function: printCalendarDate
    Description: print out the calendar date to the screen in the format: (Month-day-year-weekday)
    Inputs: 
        - day: day of the calendar month
        - month: the calendar month
        - year: the year
        - dweek: weekday
 
    Outputs:
        - None
*/
void printCalendarDate(int day, int month, int year, char* dweek, int numEvent){
    if(numEvent > 0)
        printf("\n\n");
    int strLength = 0;
    char monthArray[][12] = {"January", "February", "March", "April", "May", "June", 
                    "July", "August", "September", "October", "November", "December"};
    strLength = (int)(strlen(monthArray[month-1]));
    strLength += length(year);
    strLength += length(day);
    strLength += (int)(strlen(dweek));
    printf("%s %d, %d (%s)\n", monthArray[month-1], day, year, dweek);
    for(int i = 0; i < strLength+6; i++){
        printf("-");
    }
}

/*
    Function: findEventPos
    Description: find the position of the valid event
    Inputs:
        - output: array that stores valid event's data to be printed to the screen
        - targetDay: event of the current day to be searched
    Outputs: return the position of the event as integer
        - i: if the event has been found
        - 0: if the event has not been found
*/
int findEventPos(char output[][MAX_LINE_LEN], int targetDay){
    int curDate, day, month, yr;
    for(int i = 0; i < MAX_EVENTS && strlen(output[i])>0; i += 9){
        day = convertDate(output[i+3]);
        month = convertDate(output[i+4]);
        yr = convertDate(output[i+5]);
        curDate = createCalendarDate(day, month, yr);
        if(curDate == targetDay)
            return i;
    }
    return 0;
}

/*
    Function: display
    Description: display each valid event and its corresponding information into the console
    Inputs:
        - output: array that stores valid event's data to be printed to the screen
        - startDate: startDate from the console used for looking for valid event
        - endDate: endDate from the console used for looking for valid event
    Outputs:
        - None
*/
void display(char output[][MAX_LINE_LEN], char *startDate, char *endDate){
    int start, end, curIndex, curTime, numEvent;
    char dweek[MAX_LINE_LEN];
    curIndex = 0, numEvent = 0;
    start = createCalendarDate(convertDay(startDate), convertMth(startDate), convertYr(startDate));
    end = createCalendarDate(convertDay(endDate), convertMth(endDate), convertYr(endDate));
    //printf("%d\n", start);
    //printf("%d\n", end);
    //go over through the startdate to the end date
    for(int i = start; i <=end; i++){
        curTime = createCalendarDate(convertDay(output[curIndex+3]), convertMth(output[curIndex+4]), convertYr(output[curIndex+5]));\
        if(ValidDate(output, i)==1){
            //printf("%d\n", i); //format dates (year-month-day form) per event
            int day = i%100, mth = (i/100)%100, yr = i/10000;//create year, month and day variables
            curIndex = findEventPos(output, i);
            strcpy(dweek, output[curIndex+6]);
            printCalendarDate(day, mth, yr, dweek, numEvent);
            //printf("%d\n", curIndex);
            formatEvent(output, i, curIndex);
            curIndex += 9;
            numEvent++;
        }
    }
}

/*
    Function: readFile
    Description: read xml file and store the informations of each event into the event array
    Inputs:
        - start: startDate inputted from the console to look for events
        - end: endDate inputted from the console to look for events
        - fileName: the name of the file we need to retrive information for each event
    Outputs:
        - None
*/
void readFile(char start[], char end[], char fileName[]){
    char startDate[MAX_LINE_LEN];
    char endDate[MAX_LINE_LEN];
    char path[MAX_LINE_LEN];
    
    generateInput(startDate, start);
    generateInput(endDate, end);
    generateInput(path, fileName);

    //create a line to retrieve each line from the file with size 100 (max)
    char line[MAX_LINE_LEN];
    char info[MAX_LINE_LEN];
    
    //create a 2d char array to store informations in the xml file line by line (storing 1000 lines of strings)
    char event[MAX_EVENTS][MAX_LINE_LEN];
    int ind = 0;
    
    //create a file and read it
    FILE *file = fopen(path, "r");
    
    while(fgets(line, MAX_LINE_LEN, file)!=NULL){
        generateData(info, line);
        
        if(strlen(info)>=1){//add proper info into event array
            strcpy(event[ind], info);
            ind++;
        }
    }
    
    char output[MAX_EVENTS][MAX_LINE_LEN]; 
    findEvent(event, output, startDate, endDate);//store valid event into the output array
    display(output, startDate, endDate);
}

/*
    Function: main
    Description: represents the entry point of the program.
    Inputs: 
        - argc: indicates the number of arguments to be passed to the program.
        - argv: an array of strings containing the arguments passed to the program.
    Output: an integer describing the result of the execution of the program:
        - 0: Successful execution.
        - 1: Erroneous execution.
*/
int main(int argc, char *argv[])
{
    /* Starting calling your own code from this point. */
    // Ideally, please try to decompose your solution into multiple functions that are called from a concise main() function.

    validInput(argc);// check if the input is valid
    readFile(argv[1], argv[2], argv[3]);//read xml files

    exit(0);
}