# [_ENTER THE DATABASE_](INDEX.md)

# Zettelkasten (ZK) guidelines
 [Introduction to Zettelkasten note-taking method](https://zettelkasten.de/posts/overview/)  
  
 <details markdown='1'><summary>Useful software (Android)</summary>

 Markor, a free and versatile markdown editor: [GitHub](https://github.com/gsantner/markor), [F-Droid](https://f-droid.org/packages/net.gsantner.markor), [Google Play](https://play.google.com/store/apps/details?id=net.gsantner.markor)
 
 Termux, a unix-like environment for Android: [Official site](https://termux.com/) - for `git` and `python3` (see [common_actions.py](common_actions.py) ) to back up your ZK to the remote git storage (optional).  
 
 </details>
 
 ----
 
This is a template that represents my vision of a mobile-phone friendly markdown-based ZK. It is imperfect, but it may be useful.
 
The main key points: 
1. Stick to the main principles of ZK notes: 
- One idea per note.
- Use your own words.
- Keep it short and simple.
- Links are important.  

2. Everything should be linked both ways (links between zettels, zettels and tags, zettels and index, etc). This way one could navigate the database in any direction via the links between files seamlessly.  

4. If you need to copy/paste something - I suggest you to hide it under the spoiler (see template in the bottom).
----

The principle of contributing to ZK based on this template:  
1. Save the idea to [notepad](notepad.md), copy respective source link if required.
2. Entries for future research go to the [todo](todo.txt).
3. Review, revise, prepare the draft of a zettel from the note.  
4. Create a file for zettel `name_it_like_this.md` in the `ZETTELS` folder.  
5. Link zettel with other zettels.  
6. Link other zettels to the zettel.  
7. Optional: Insert sources.  
8. Optional: Link zettel to a tag (create a respective tag .md file in `TAGS` folder, and link it to zettel, and link zettel to the tag.  
9. Optional: Insert supplementary data (copy-pasta, for instance)

If adding a new entry-point (topic) zettel:  
1. Link zettel in one of the catalogue lists in `INDEX` folder.  
2. If necessary - create a new catalogue and link it to [the main INDEX](INDEX.md)


# Template

### Title (name)

Text

<details markdown='1'><summary>Expand / Collapse</summary>

### links
1. link1 - description
2. link2 - description

### sources
>source1  
>source2

### supplementary
<details markdown='1'><summary>Expand / Collapse</summary>
Some additional data, such as quotes, numbers, links to images, etc, etc...
</details>

### tags
tag1, tag2

</details>
