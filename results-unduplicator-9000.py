file = open("scouting.tsv", "r")
try:
    out_file = open("scouting_2.tsv", "w")
except:
    out_file = open("scouting_2.tsv", "c")
write_lines = []
lines = []
num_dupes = 0
num_copied = 0

for line in file.readlines():
    duplicate = False
    for line_line in lines:
        if line == line_line:
            duplicate = True
    lines.append(line)
    if not duplicate:
        write_lines.append(line)
        num_copied += 1
    else:
        num_dupes += 1
    print("Duplicates: " + str(num_dupes) + "Copied: " + str(num_copied))
out_file.writelines(write_lines)
file.close()
out_file.close()
