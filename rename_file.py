import os, time

from collections import defaultdict

target_dir = "/Users/ahnsukyum/Desktop/230423_옥상에서"
os.chdir(target_dir)
file_rename = "from_the_rooftop"

pic_file_names_sets = []
i=0
file_names = os.listdir()
file_names.sort(key=lambda x: (time.ctime(os.path.getmtime(x)),x))

print(file_names)
for filename in file_names:
    if os.path.splitext(filename)[1] == '.JPG':
        pic_file_names_sets.append((filename, f'{file_rename + "_" + str(i).zfill(4)}'))
        i+=1

print(pic_file_names_sets)
for t in pic_file_names_sets:

        if os.path.exists(t[0]+".JPG"):
            print("file name " +t+ " exists")
        else :
            try:
                os.rename(f'{target_dir + "/" + t[0]}',
                           f'{target_dir + "/" + t[1] + ".JPG"}')
                print(f"renamed {t[0]} as {t[1]}.JPG ")
            except (FileNotFoundError) as e:
                print("----"+str(e))

for t in pic_file_names_sets:
        if os.path.exists(t[0]+"ARW"):
            print("file name " + t + " exists")
        else:
            try:

                os.rename(f'{target_dir + "/" + t[0][:-4] + ".ARW"}',
                          f'{target_dir + "/" + t[1] + ".ARW"}')
                print(f"renamed {t[0][:-4] + '.ARW'} as {t[1]}.ARW ")
            except (FileNotFoundError) as e:
                print("----"+str(e))





