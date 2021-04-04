string = "hello i am heeth.i am a boy"

ans_bullets = string.split('.')

new_list = []

print(ans_bullets)
print()

new_list = []
for ans_bullet in ans_bullets:
    print(ans_bullet)
    ele = ans_bullet.split()
    new_list.append(ele)

print()
print(new_list)

#match_unfiltered = list(question.get_match_percentage(ans_bullets))
#match = match_unfiltered[0:len(keywords)]
#print("Keywords:", keywords)
#print("Answer:", ans_bullets)
#print("Match:", match)
#print()