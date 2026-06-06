import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from questions.models import Question

questions_data = [

    # ─────────────────────────────
    # DSA — Easy
    # ─────────────────────────────
    {
        'question_text': 'What is the time complexity of binary search?',
        'category': 'dsa',
        'difficulty': 'easy',
        'company': 'general',
        'model_answer': 'O(log n) because we divide the search space in half each time.',
        'tags': ['binary search', 'complexity']
    },
    {
        'question_text': 'Explain the difference between stack and queue.',
        'category': 'dsa',
        'difficulty': 'easy',
        'company': 'general',
        'model_answer': 'Stack follows LIFO (Last In First Out) while Queue follows FIFO (First In First Out).',
        'tags': ['stack', 'queue', 'data structures']
    },
    {
        'question_text': 'What is a linked list and how does it differ from an array?',
        'category': 'dsa',
        'difficulty': 'easy',
        'company': 'tcs',
        'model_answer': 'Linked list stores elements in nodes with pointers. Arrays store elements in contiguous memory. Linked lists have O(1) insertion but O(n) access while arrays have O(1) access but O(n) insertion.',
        'tags': ['linked list', 'array']
    },
    {
        'question_text': 'What is recursion? Give an example.',
        'category': 'dsa',
        'difficulty': 'easy',
        'company': 'infosys',
        'model_answer': 'Recursion is when a function calls itself. Example: factorial(n) = n * factorial(n-1)',
        'tags': ['recursion']
    },

    # ─────────────────────────────
    # DSA — Medium
    # ─────────────────────────────
    {
        'question_text': 'Given an array of integers, find two numbers that add up to a target sum.',
        'category': 'dsa',
        'difficulty': 'medium',
        'company': 'flipkart',
        'model_answer': 'Use a hash map to store complement values. For each element check if target-element exists in map. O(n) time O(n) space.',
        'tags': ['array', 'hash map', 'two sum']
    },
    {
        'question_text': 'How would you detect a cycle in a linked list?',
        'category': 'dsa',
        'difficulty': 'medium',
        'company': 'amazon',
        'model_answer': 'Use Floyd\'s cycle detection algorithm with slow and fast pointers. If they meet, cycle exists.',
        'tags': ['linked list', 'cycle detection']
    },
    {
        'question_text': 'Explain merge sort and its time complexity.',
        'category': 'dsa',
        'difficulty': 'medium',
        'company': 'google',
        'model_answer': 'Merge sort divides array in half recursively then merges sorted halves. Time O(n log n), Space O(n).',
        'tags': ['sorting', 'divide and conquer']
    },
    {
        'question_text': 'What is a binary search tree? What are its properties?',
        'category': 'dsa',
        'difficulty': 'medium',
        'company': 'microsoft',
        'model_answer': 'BST is a tree where left child < parent < right child. Search, insert, delete are O(h) where h is height.',
        'tags': ['tree', 'bst']
    },

    # ─────────────────────────────
    # DSA — Hard
    # ─────────────────────────────
    {
        'question_text': 'Solve the longest common subsequence problem.',
        'category': 'dsa',
        'difficulty': 'hard',
        'company': 'google',
        'model_answer': 'Use dynamic programming. dp[i][j] = length of LCS of first i chars of s1 and j chars of s2.',
        'tags': ['dynamic programming', 'string']
    },
    {
        'question_text': 'Find the maximum sum subarray using Kadane\'s algorithm.',
        'category': 'dsa',
        'difficulty': 'hard',
        'company': 'flipkart',
        'model_answer': 'Kadane\'s algorithm: keep track of current sum and max sum. Reset current sum to 0 when it becomes negative.',
        'tags': ['array', 'dynamic programming']
    },

    # ─────────────────────────────
    # System Design
    # ─────────────────────────────
    {
        'question_text': 'Design a URL shortener like bit.ly.',
        'category': 'system_design',
        'difficulty': 'medium',
        'company': 'flipkart',
        'model_answer': 'Use hash function to generate short code. Store mapping in DB. Use cache for frequent URLs. Consider load balancing and CDN.',
        'tags': ['system design', 'hashing', 'cache']
    },
    {
        'question_text': 'How would you design WhatsApp messaging system?',
        'category': 'system_design',
        'difficulty': 'hard',
        'company': 'microsoft',
        'model_answer': 'Use WebSocket for real-time messaging. Message queue for reliability. NoSQL for messages. CDN for media.',
        'tags': ['system design', 'websocket', 'messaging']
    },
    {
        'question_text': 'Design a food delivery system like Zomato.',
        'category': 'system_design',
        'difficulty': 'hard',
        'company': 'zomato',
        'model_answer': 'Microservices for orders, restaurants, delivery. Real-time location tracking with WebSocket. Redis for caching menus.',
        'tags': ['system design', 'microservices']
    },

    # ─────────────────────────────
    # Core CS
    # ─────────────────────────────
    {
        'question_text': 'What is the difference between process and thread?',
        'category': 'core_cs',
        'difficulty': 'easy',
        'company': 'tcs',
        'model_answer': 'Process is independent execution unit with own memory. Thread is lightweight unit sharing memory within process.',
        'tags': ['os', 'process', 'thread']
    },
    {
        'question_text': 'Explain ACID properties in databases.',
        'category': 'core_cs',
        'difficulty': 'medium',
        'company': 'infosys',
        'model_answer': 'Atomicity, Consistency, Isolation, Durability. Ensures reliable database transactions.',
        'tags': ['dbms', 'acid', 'transactions']
    },
    {
        'question_text': 'What is indexing in databases and why is it used?',
        'category': 'core_cs',
        'difficulty': 'medium',
        'company': 'razorpay',
        'model_answer': 'Index is data structure that improves query speed. Uses B-tree or hash. Speeds up reads but slows writes.',
        'tags': ['dbms', 'indexing']
    },
    {
        'question_text': 'Explain TCP vs UDP.',
        'category': 'core_cs',
        'difficulty': 'easy',
        'company': 'wipro',
        'model_answer': 'TCP is reliable, connection-oriented, ordered delivery. UDP is faster, connectionless, no guarantee of delivery.',
        'tags': ['networking', 'tcp', 'udp']
    },

    # ─────────────────────────────
    # HR — India Specific
    # ─────────────────────────────
    {
        'question_text': 'Tell me about yourself.',
        'category': 'hr',
        'difficulty': 'easy',
        'company': 'general',
        'model_answer': 'Structure: Current status, education, key skills, projects, why this company.',
        'tags': ['hr', 'introduction']
    },
    {
        'question_text': 'Why do you want to join our company?',
        'category': 'hr',
        'difficulty': 'easy',
        'company': 'general',
        'model_answer': 'Research company values, products, culture. Align with personal goals.',
        'tags': ['hr', 'motivation']
    },
    {
        'question_text': 'Where do you see yourself in 5 years?',
        'category': 'hr',
        'difficulty': 'easy',
        'company': 'tcs',
        'model_answer': 'Show growth mindset, technical leadership goals, alignment with company vision.',
        'tags': ['hr', 'career goals']
    },
    {
        'question_text': 'What is your greatest weakness?',
        'category': 'hr',
        'difficulty': 'medium',
        'company': 'infosys',
        'model_answer': 'Pick genuine weakness, show self awareness and steps taken to improve it.',
        'tags': ['hr', 'self awareness']
    },
    {
        'question_text': 'Describe a challenging project you worked on.',
        'category': 'hr',
        'difficulty': 'medium',
        'company': 'flipkart',
        'model_answer': 'Use STAR method: Situation, Task, Action, Result. Be specific with metrics.',
        'tags': ['hr', 'star method', 'behavioral']
    },

    # ─────────────────────────────
    # Startup Specific
    # ─────────────────────────────
    {
        'question_text': 'How do you handle ambiguity and undefined requirements?',
        'category': 'hr',
        'difficulty': 'medium',
        'company': 'startup',
        'model_answer': 'Ask clarifying questions, break down problem, make assumptions explicit, iterate fast.',
        'tags': ['startup', 'problem solving']
    },
    {
        'question_text': 'Tell me about a time you learned something new quickly.',
        'category': 'hr',
        'difficulty': 'easy',
        'company': 'razorpay',
        'model_answer': 'Show learning agility. Describe situation, what you learned, how fast, result.',
        'tags': ['learning', 'growth mindset']
    },
]


def populate():
    count = 0
    for q in questions_data:
        obj, created = Question.objects.get_or_create(
            question_text=q['question_text'],
            defaults={
                'category': q['category'],
                'difficulty': q['difficulty'],
                'company': q['company'],
                'model_answer': q['model_answer'],
                'tags': q['tags']
            }
        )
        if created:
            count += 1
            print(f" Added: {q['question_text'][:50]}")
        else:
            print(f" Already exists: {q['question_text'][:50]}")

    print(f"\n Done! Added {count} new questions")
    print(f" Total questions in DB: {Question.objects.count()}")


if __name__ == '__main__':
    populate()