# Model Example

原文<href>https://simpleisbetterthancomplex.com/series/2017/09/11/a-complete-beginners-guide-to-django-part-2.html<href>

##Introduction

我們的項目是一個討論區（一個論壇）。 整個想法是維護幾個板，其行為類似於類別。 然後，在特定的板內，用戶可以通過創建新主題來開始新的討論。 在本主題中，其他用戶可以參與討論發布回覆。</br>
我們需要找到一種方法來區分常規用戶和管理員用戶，因為只有管理員應該創建新的主板。 下面是我們主要用例的概述以及每種用戶的角色：</br>
<img src="Diagram.png" alt="Smiley face" height="42" width="42">