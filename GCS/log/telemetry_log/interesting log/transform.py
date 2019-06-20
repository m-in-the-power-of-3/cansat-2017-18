

log = open("./telemetry_log_4.txt", 'r')
log_3 = open("./telemetry_log_3.txt", 'w')

ist = log
pri = log_3

a = -1
data = []
try:
    while True:
        a += 1
        data.append(log.readline())
        if a == 37135:

            print("end____________________________________")
            break

    a = -1
    while True:
        a += 1
        data[a] = data[a].replace("WAIT_SIGNAL", " 0 ")
        data[a] = data[a].replace("STATE_WAIT_SEPARATION", " 1 ")
        data[a] = data[a].replace("MAIN_PART", " 2 ")

        data[a] = data[a].replace(",", ".")
        data[a] = data[a].replace("    ", ",")
        data[a] = data[a].replace("   ", ",")
        data[a] = data[a].replace("  ", ",")
        data[a] = data[a].replace(" ", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")
        data[a]= data[a].replace(",,", ",")

        print(data[a])
        if a == 37135:
            print("end____________________________________")
            break
    a = -1
    while True:
        a += 1
        #log_3.write("llol\n")
        log_3.write(data[a])
        if a == 37135:
            print("end____________________________________")
            break




except:
    log.close()
    log_3.close()
    raise



