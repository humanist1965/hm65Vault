import re

tagToSearch = "t" + "[^ ]*[ ]"
res = re.findall(tagToSearch, "tag1 tag2 tag3 ", re.IGNORECASE)
print(type(res))
print(res)