# How to Implement CRUD Using Ajax and Json

<a href = "https://simpleisbetterthancomplex.com/tutorial/2016/11/15/how-to-implement-a-crud-using-ajax-and-json.html">原文</a>



## view
```python 

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Book.objects.all()
            data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
                'books': books
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
    else:
        form = BookForm()
    return save_book_form(request, form, 'books/includes/partial_book_create.html')


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
    else:
        form = BookForm(instance=book)
    return save_book_form(request, form, 'books/includes/partial_book_update.html')
```
## js

```javascript

$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book .modal-content").html("");
        $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#book-table tbody").html(data.html_book_list);
          $("#modal-book").modal("hide");
        }
        else {
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-create-book").click(loadForm);
  $("#modal-book").on("submit", ".js-book-create-form", saveForm);

  // Update book
  $("#book-table").on("click", ".js-update-book", loadForm);
  $("#modal-book").on("submit", ".js-book-update-form", saveForm);

  // Delete book
  $("#book-table").on("click", ".js-delete-book", loadForm);
  $("#modal-book").on("submit", ".js-book-delete-form", saveForm);

});

```





## template

#### listview

book_list.html
```html
{% extends 'base.html' %}
{% load static %}

{% block javascript %}
  <script src="{% static 'books/js/books.js' %}"></script>
{% endblock %}
{% block content %}
  <h1 class="page-header">Books</h1>
  <p>
    <button type="button" class="btn btn-primary js-create-book">
      <span class="glyphicon glyphicon-plus"></span>
      New book
    </button>
  </p>
  <table class="table" id="book-table">
    <thead>
      <tr>
        <th>#</th>
        <th>Title</th>
        <th>Author</th>
        <th>Type</th>
        <th>Publication date</th>
        <th>Pages</th>
        <th>Price</th>
      </tr>
    </thead>
    <tbody>
        {% include 'books/includes/partial_book_list.html' %}
    </tbody>
  </table>
  <div class="modal fade" id="modal-book">
    <div class="modal-dialog">
      <div class="modal-content">
      </div>
    </div> 
  
{% endblock %}
```

```html
partial_book_list.html
{% for book in books %}
  <tr>
    <td>{{ book.id }}</td>
    <td>{{ book.title }}</td>
    <td>{{ book.author }}</td>
    <td>{{ book.get_book_type_display }}</td>
    <td>{{ book.publication_date }}</td>
    <td>{{ book.pages }}</td>
    <td>{{ book.price }}</td>
    <td>
      <button type="button"
              class="btn btn-warning btn-sm js-update-book"
              data-url="{% url 'book_update' book.id %}">
        <span class="glyphicon glyphicon-pencil"></span> Edit
      </button>
    </td>
  </tr>
{% empty %}
  <tr>
    <td colspan="8" class="text-center bg-warning">No book</td>
  </tr>
{% endfor %}
```
#### partial_book_form
```
{% load widget_tweaks %}

{% for field in form %}
  <div class="form-group{% if field.errors %} has-error{% endif %}">
    <label for="{{ field.id_for_label }}">{{ field.label }}</label>
    {% render_field field class="form-control" %}
    {% for error in field.errors %}
      <p class="help-block">{{ error }}</p>
    {% endfor %}
  </div>
{% endfor %
```

#### partial_book_create
```html
<form method="post" action="{% url 'book_create' %}" class="js-book-create-form">
  {% csrf_token %}
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
    <h4 class="modal-title">Create a new book</h4>
  </div>
  <div class="modal-body">
    {% include 'books/includes/partial_book_form.html' %}
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
    <button type="submit" class="btn btn-primary">Create book</button>
  </div>
</form>
```

#### partial_book_update.html

```html
<form method="post" action="{% url 'book_update' form.instance.pk %}" class="js-book-update-form">
  {% csrf_token %}
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
    <h4 class="modal-title">Update book</h4>
  </div>
  <div class="modal-body">
    {% include 'books/includes/partial_book_form.html' %}
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
    <button type="submit" class="btn btn-primary">Update book</button>
  </div>
</form
```

