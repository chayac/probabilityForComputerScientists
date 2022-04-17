#!/usr/bin/env python

# make sure to run 
# > python -m pip install bottle
# I used version bottle-0.12.19
from bottle import SimpleTemplate
from bs4 import BeautifulSoup
import json
import hjson

import os.path
import sys

IGNORE_DIRS = [
]
TEMPLATE_DIR = 'chapters'
ROOT = 'pythonreader'
OUT_DIR = 'en'

# Use the -t flag if you want to compile for local tests
DEPLOY = False

class DefinitionBuilder(object):

    # Function: Run
    # -------------
    # This function compiles all the html files (recursively)
    # from the templates dir into the current folder. Folder
    # hierarchy is preserved
    def run(self):
        header = r"""
        <!DOCTYPE html>
        <html>

        <head>
            

            <title>{{title or 'Probability for Computer Scientists'}}</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<meta http-equiv="content-type" content="text/html; charset=UTF8">

<link rel="shortcut icon" type="image/x-icon" href="{{pathToRoot}}favicon.ico">

<!-- Python highlighting -->
<script src="{{pathToRoot}}plugins/prism/prism.js"></script>
<link href="{{pathToRoot}}plugins/prism/prism.css" rel="stylesheet" />

<!-- jQuery CDN -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js" integrity="sha512-uto9mlQzrs59VwILcLiRYeLKPPbS/bT71da/OEBYEwcdNUk8jYIy+D176RYoop1Da+f9mvkYrmj5MCLZWEtQuA==" crossorigin="anonymous"></script>
 <link href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/base/jquery-ui.css" rel="Stylesheet" type="text/css" />

<!-- D3 CDN -->
<script src="https://d3js.org/d3.v3.js"></script>
<!-- <script src="https://d3js.org/d3.v4.js"></script> -->
<script src="https://d3js.org/d3-scale-chromatic.v1.min.js"></script>

<!-- Chart CDN -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.6.0/dist/chart.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-annotation/1.0.2/chartjs-plugin-annotation.min.js" integrity="sha512-FuXN8O36qmtA+vRJyRoAxPcThh/1KJJp7WSRnjCpqA+13HYGrSWiyzrCHalCWi42L5qH1jt88lX5wy5JyFxhfQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>

<!-- PDF JS -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.6.347/pdf.min.js" integrity="sha512-Z8CqofpIcnJN80feS2uccz+pXWgZzeKxDsDNMD/dJ6997/LSRY+W4NmEt9acwR+Gt9OHN0kkI1CTianCwoqcjQ==" crossorigin="anonymous"></script>

<!-- Lunr CDN -->
 <script src="https://unpkg.com/lunr@2.0.4/lunr.js"></script>

<!-- Firebase CDN -->
<script src='https://cdn.firebase.com/js/client/2.2.1/firebase.js'></script>

<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<link rel="stylesheet" type="text/css" href="{{pathToRoot}}css/style.css">

<!-- Firebase App (the core Firebase SDK) is always required and must be listed first -->
  <script src="https://www.gstatic.com/firebasejs/8.1.2/firebase-app.js"></script>

  <!-- If you enabled Analytics in your project, add the Firebase SDK for Analytics -->
  <script src="https://www.gstatic.com/firebasejs/8.1.2/firebase-analytics.js"></script>

  <!-- Add Firebase products that you want to use -->
  <script src="https://www.gstatic.com/firebasejs/8.1.2/firebase-auth.js"></script>
  <script src="https://www.gstatic.com/firebasejs/8.1.2/firebase-firestore.js"></script>


   

<!-- Java Script -->
<script src="{{pathToRoot}}plugins/moment.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

<!-- Python highlighting -->
<script src="{{pathToRoot}}plugins/prism/prism.js"></script>
<link href="{{pathToRoot}}plugins/prism/prism.css" rel="stylesheet" />

<!-- Probability Packages -->
<script src="{{pathToRoot}}js/probabilityUtils.js"></script>
<script src="{{pathToRoot}}plugins/probability/gaussian.js"></script>
<script src="{{pathToRoot}}plugins/color.js"></script>
<script src='https://cdn.jsdelivr.net/npm/jstat@latest/dist/jstat.min.js'></script>


<!-- font awesome -->
	<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.0/css/all.css" integrity="sha384-lZN37f5QGtY3VHgisS14W3ExzMWZxybE1SJSEsQp9S+oqd12jhcu+A56Ebc1zFSJ" crossorigin="anonymous">

<!-- SWAL -->
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>


<!-- Stanford -->
<link href='https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600,700' rel='stylesheet' type='text/css'>
<link href='https://fonts.googleapis.com/css?family=Source+Serif+Pro:400,600,700' rel='stylesheet' type='text/css'>
<link href="https://fonts.googleapis.com/css?family=Crimson+Text" rel="stylesheet">

<!-- Math Jax -->
<!-- <script type="text/x-mathjax-config">
  MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
</script> -->
<script type="text/javascript">
  MathJax = {
    config: ["MMLorHTML.js"],
    jax: ["input/TeX","input/MathML","output/HTML-CSS","output/NativeMML"],
    extensions: ["tex2jax.js","mml2jax.js","MathMenu.js","MathZoom.js", "fast-preview.js"],
    TeX: {
      extensions: ["AMSmath.js","AMSsymbols.js","noErrors.js","noUndefined.js", "action.js"]
    },
    tex: {
      inlineMath: [ ['$','$'], ["\\(","\\)"] ],
      processEscapes: true
    },
	"fast-preview": {
	  disabled: true
	}
  };
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>



<script src="{{pathToRoot}}plugins/math.min.js"></script>



    <!-- Popper.JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
    <!-- Bootstrap JS -->
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>

 <!-- Scrollbar Custom CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar.min.css">
    <script src="{{pathToRoot}}plugins/jquery.mCustomScrollbar.js"></script>


        </head>

        <script>
        Chart.defaults.font.family = 'Times New Roman';
        Chart.defaults.font.size = 18;
        </script>


        <!-- I declare a few math operators I often use in equations -->
        <div style="display:none">
        $\DeclareMathOperator{\p}{P}$
        $\DeclareMathOperator{\P}{P}$
        $\DeclareMathOperator{\c}{^C}$
        $\DeclareMathOperator{\or}{  or}$
        $\DeclareMathOperator{\and}{  and}$
        $\DeclareMathOperator{\var}{Var}$
        $\DeclareMathOperator{\Var}{Var}$
        $\DeclareMathOperator{\Std}{Std}$
        $\DeclareMathOperator{\E}{E}$
        $\DeclareMathOperator{\std}{Std}$
        $\DeclareMathOperator{\Ber}{Bern}$
        $\DeclareMathOperator{\Bin}{Bin}$
        $\DeclareMathOperator{\Poi}{Poi}$
        $\DeclareMathOperator{\Uni}{Uni}$
        $\DeclareMathOperator{\Geo}{Geo}$
        $\DeclareMathOperator{\NegBin}{NegBin}$
        $\DeclareMathOperator{\Beta}{Beta}$
        $\DeclareMathOperator{\Exp}{Exp}$
        $\DeclareMathOperator{\N}{N}$
        $\DeclareMathOperator{\R}{\mathbb{R}}$
        $\DeclareMathOperator*{\argmax}{arg\,max}$
        $\newcommand{\d}{\, d}$
        
        </div>

        <body>
        <div class="wrapper">
        <div id="content">
        
         <div class="container-sm">
                <div class="row d-flex justify-content-center">
                    <div class="col-sm handout" >
        """

        footer = r"""</div></div></div></body></html>"""
        with open("definitions.html", "w") as self.defFile:
            # defFile = open("definitions.html", "w")
            self.defFile.write(header)
            # defFile.close()

            self.index = []
            book_data = hjson.load(open('bookOutline.hjson'))
            for part_key, part in book_data.items():
                if part_key == "intro": continue
                self.defFile.write("<h2>" + part['title'] + "</h2>")
                for section_key, title in part['sections'].items():
                    # section_title = "<h2>" + part_key + section_key + "</h2>\n"
                    # print(part_key, section_key)
                    # defFile = open("definitions.html", "a")
                    # defFile.write(section_title)
                    # defFile.close()
                    path = '{}/{}'.format(part_key, section_key)
                    self.addSectionToIndex(path, section_key, title)
            # defFile = open("definitions.html", "a")
            self.defFile.write(footer)
            # defFile.close()
            # json.dump(self.index,open('searchIndex.json', 'w'))

    #####################
    # Private Helpers
    #####################

    def addSectionToIndex(self, rel_path, key, title):
        sectionDirPath = os.path.join(TEMPLATE_DIR, rel_path)
        for fileName in os.listdir(sectionDirPath):
            if fileName.endswith('.html'):
                filePath = os.path.join(sectionDirPath, fileName)
                self.addFileToIndex(filePath, rel_path, key, title)

    def addFileToIndex(self, filePath, url, key, title):
        print(filePath)
        templateText = open(filePath).read()
        section_title = "<h3>" + title + "</h3>\n"
        # compiledHtml = SimpleTemplate(templateText).render(pathToRoot = '../' + pathToLangRoot, pathToLang = pathToLangRoot)
        soup = BeautifulSoup(templateText, 'html.parser')
        # defFile = open("definitions.html", "a")
        defs = soup.find_all("div", "bordered")
        if defs == []: return
        self.defFile.write(section_title)
        for def1 in defs:
            self.defFile.writelines(def1.prettify())
        # templateText.close()
        # defFile.writelines(soup.find_all("div", "bordered"))
        # defFile.close()
        # print(soup.prettify())
        # print(soup.find_all(name="div", attr={"class": "bordered"}, recursive=True))
        # newItem = {
        #     'id':key,
        #     'title':title,
        #     'url':url,
        #     'text':self.sanitizeText(soup.get_text())
        # }
        # self.index.append(newItem)
        

    def sanitizeText(self, text):
        sText = ''
        for line in text.split('\n'):
            stripped = line.strip()
            if stripped.startswith('%'):
                continue
            sText += line + '\n'
        return sText


if __name__ == '__main__':
    DefinitionBuilder().run()
