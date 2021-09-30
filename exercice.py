#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_instances(text: str, word) -> tuple:
	len_word = len(word)
	return tuple(index for index in range(len(text)-len_word+1) if text[index:index+len_word] == word)

def keep_words(text, liste):
	new_txt = ""
	
	for x in range(len(text)):
		for y, z in {word:len(word) for word in liste}.items():
			try:
				if y == text[x:x+z]:
					new_txt+=y
			except:
				pass

	return new_txt

def check_brackets(text, brackets):
	liste, brackets = "".join([letter for letter in text if letter in brackets]), "".join(brackets)
	pre_lenght = 0
	while len(liste)!=pre_lenght:
		pre_lenght = len(liste)
		for x in range(0,5,2):
			liste = liste.replace(brackets[x:x+2], "")
	return not bool(liste)

def remove_comments(full_text, comment_start, comment_end):
	full_text = full_text.replace(comment_start, "¹").replace(comment_end, "²")
	i=0
	text = ""
	for lettre in full_text:
		if lettre == "¹":
			i+=1
		elif lettre == "²":
			i-=1
		elif i==0:
			text+=lettre
		elif i<0:
			return None

	return text if not i else None
		

def get_tag_prefix(text, opening_tags, closing_tags):
	for open in opening_tags:
		if 0 in get_instances(text,open):
			return (open,None)
	for close in closing_tags:
		if 0 in get_instances(text, close):
			return (None,close)
	return (None, None)

def check_tags(full_text, group_tag_names, text_tag_names, comment_tags):
	liste = remove_comments("".join(full_text).replace(" ", "").replace("<br>","").replace("<head/>", ""),comment_tags[0],comment_tags[1])
	if not liste:
		return False
	if isinstance(text_tag_names, tuple):
		for x in text_tag_names:
			liste = remove_comments(liste, f"<{x}>", f"</{x}>")
	else:
		liste = remove_comments(liste, f"<{text_tag_names}>", f"</{text_tag_names}>")
	if not liste:
		return False
		
	tag_names = ["<"+tag+"></"+tag+">" for tag in group_tag_names]
	pre_lenght = 0
	while len(liste)!=pre_lenght:
		pre_lenght = len(liste)
		for x in tag_names:
			liste = liste.replace(x, "")
	return not bool(liste)


if __name__ == "__main__":
	brackets = ("(", ")", "{", "}")
	yeet = "(yeet){yeet{}}[]"
	yeeet = "({yeet})"
	yeeeet = "({yeet)}"
	yeeeeet = "(yeet"
	print(check_brackets(yeet,brackets))
	print(check_brackets(yeeet,brackets))
	print(check_brackets(yeeeet,brackets))
	print(check_brackets(yeeeeet,brackets))
	print()

	spam = "Hello, /* OOGAH BOOGAH */world!"
	eggs = "Hello, /* OOGAH BOOGAH world!"
	parrot = "Hello, OOGAH BOOGAH*/ world!"
	print(remove_comments(spam, "/*", "*/"))
	print(remove_comments(eggs, "/*", "*/"))
	print(remove_comments(parrot, "/*", "*/"))
	print()

	otags = ("<head>", "<body>", "<h1>")
	ctags = ("</head>", "</body>", "</h1>")
	print(get_tag_prefix("<body><h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("<h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("</h1></body>", otags, ctags))
	print(get_tag_prefix("</body>", otags, ctags))
	print()

	spam = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"    </title>"
		"  </head>"
		"  <body>"
		"    <h1>Hello, world</h1>"
		"    <!-- Les tags vides sont ignorés -->"
		"    <br>"
		"    <h1/>"
		"  </body>"
		"</html>"
	)
	eggs = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    <!-- Il manque un end tag"
		"    </title>-->"
		"  </head>"
		"</html>"
	)
	parrot = (
		"<html>"
		"  <head>"
		"    <title>"
		"      Commentaire mal formé -->"
		"      Example"
		"    </title>"
		"  </head>"
		"</html>"
	)
	group_tags = ("html", "head", "title", "body")
	text_tags = ("h1")
	comment_tags = ("<!--", "-->")
	print(check_tags(spam, group_tags, text_tags, comment_tags))
	print(check_tags(eggs, group_tags, text_tags, comment_tags))
	print(check_tags(parrot, group_tags, text_tags, comment_tags))
	print()
