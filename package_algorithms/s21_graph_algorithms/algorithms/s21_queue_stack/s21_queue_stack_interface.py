"""Interface for C++ queue and stack dynamic library"""

import cppyy
import pathlib

cppyy.cppdef(
    """
namespace s21 {
template <typename T>
class list {
 public:
  //  List Member type
  using value_type = T;
  using reference = T&;
  using const_reference = const T&;
  using size_type = std::size_t;

 private:
  struct Node {
    T value_;
    Node* prev_;
    Node* next_;
    Node(const T& value) : value_(value), prev_(nullptr), next_(nullptr) {}
  };

  Node* head_;
  Node* tail_;
  Node* end_;
  size_type size_;

  // ================================================================
  // ================================================================
  //  List Iterator Internal Class
  template <typename value_type>
  class ListIterator {
   public:
    ListIterator() { ptr_ = nullptr; }
    ListIterator(Node* ptr) : ptr_(ptr){};
    ListIterator operator++(int) { return ptr_ = ptr_->next_, *this; }
    ListIterator operator--(int) { return ptr_ = ptr_->prev_, *this; }
    ListIterator& operator++() { return ptr_ = ptr_->next_, *this; }
    ListIterator& operator--() { return ptr_ = ptr_->prev_, *this; }
    ListIterator operator+(const size_type val) { return move(val, true); }
    ListIterator operator-(const size_type val) { return move(val, false); }
    bool operator==(ListIterator other) { return ptr_ == other.ptr_; }
    bool operator!=(ListIterator other) { return ptr_ != other.ptr_; }
    reference operator*() {
      if (!ptr_) throw std::invalid_argument("Value is nullptr");
      return ptr_->value_;
    }

   private:
    Node* ptr_ = nullptr;
    friend class list<T>;

    ListIterator move(size_type val, bool fwd = true) {
      Node* tmp = ptr_;
      for (size_type i = 0; i < val; ++i) tmp = (fwd ? tmp->next_ : tmp->prev_);
      return ListIterator(tmp);
    }
  };

  // ================================================================
  //  List Const Iterator Internal Class
  template <typename value_type>
  class ListConstIterator : public ListIterator<T> {
   public:
    ListConstIterator(ListIterator<T> other) : ListIterator<T>(other) {}
    // const T& operator*() { return ListIterator<T>::operator*(); }
  };
  // ================================================================
  // ================================================================

 public:
  // List Member Functions
  list();
  list(size_type n);
  list(std::initializer_list<value_type> const& items);
  list(const list& l);
  list(list&& l);
  ~list();
  list& operator=(list&& l);

  //  List Member type (iterators)
  using iterator = ListIterator<T>;
  using const_iterator = ListConstIterator<T>;
  using it = iterator;
  using c_it = const_iterator;

  // List Iterators
  it begin() { return !head_ ? it(end_) : it(head_); }
  it end() { return it(end_); }
  c_it begin() const { return !head_ ? c_it(end_) : c_it(head_); }
  c_it end() const { return c_it(end_); }

  // List Element access
  const_reference front() const {
    return !head_ ? end_->value_ : head_->value_;
  }
  const_reference back() const { return !tail_ ? end_->value_ : tail_->value_; }

  // List Capacity
  bool empty() const { return size_ == 0; }
  size_type size() const { return size_; }
  size_type max_size() const { return (PTRDIFF_MAX / sizeof(Node)); }

  // List Modifiers
  void clear();
  void pop_front();
  void pop_back();
  void push_front(const_reference value);
  void push_back(const_reference value);
  void swap(list& other);
  iterator insert(iterator pos, const_reference value);
  void erase(iterator pos);
  void merge(list& other);
  void reverse();
  void unique();
  void sort();
  void splice(const_iterator pos, list& other);

  template <class... Args>
  iterator insert_many(const_iterator pos, Args&&... args);
  template <class... Args>
  void insert_many_back(Args&&... args);
  template <class... Args>
  void insert_many_front(Args&&... args);

 private:
  // Supplementary
  void reset();
  void update();
  void copy(const list& l);
  void pop(Node*& node);
  void push(const_reference value, bool front);
  void sort_nodes(iterator left, iterator right);
};

class queue {
 private:
  list<int> container;

 public:
  // members
  using value_type = int;
  using reference = int &;
  using const_reference = const int &;
  using size_type = size_t;

  // constructors, destructor
  queue();
  queue(std::initializer_list<value_type> const &items);
  queue(const queue &s);
  queue(queue &&s);
  queue &operator=(queue &&s);
  virtual ~queue() = default;

  // accessors
  const_reference front();
  const_reference back();

  // capacity
  bool empty() const;
  size_type size() const;

  // modifiers
  void push(const_reference value);
  void pop();
  void swap(queue &other);

};

class stack {
 private:
  list<int> container;

 public:
  // member types
  using value_type = int;
  using reference = int &;
  using const_reference = const int &;
  using size_type = size_t;

  // constructors, destructor
  stack();
  stack(std::initializer_list<value_type> const &items);
  stack(const stack &s);
  stack(stack &&s);
  stack &operator=(stack &&s);

  virtual ~stack() = default;

  // accessors
  const_reference top() const;

  // accessors
  bool empty() const;
  size_type size() const;

  // modifiers
  void push(const_reference value);
  void pop();
  void swap(stack &other) noexcept;

};

}"""
)

cppyy.load_library(str(pathlib.Path(__file__).parent.joinpath("s21_queue.so")))
cppyy.load_library(str(pathlib.Path(__file__).parent.joinpath("s21_stack.so")))

from cppyy.gbl import s21


class Queue(s21.queue):
    """Pytnon queue interface for C++ queue"""

    def pop(self):
        """Pop funtion should return a value"""

        res = super().front()
        super().pop()
        return res


class Stack(s21.stack):
    """Pytnon stack interface for C++ stack"""

    def pop(self):
        """Pop funtion should return a value"""

        res = super().top()
        super().pop()
        return res
