import psycopg2
import os

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxPathSum(root):
    def helper(node):
        nonlocal max_sum
        if not node:
            return 0
        left = max(helper(node.left), 0)
        right = max(helper(node.right), 0)
        current_sum = node.val + left + right
        max_sum = max(max_sum, current_sum)
        return node.val + max(left, right)
    max_sum = float('-inf')
    helper(root)
    return max_sum

def buildTree(values):
    if not values:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while i < len(values):
        current = queue.pop(0)
        if values[i] is not None:
            current.left = TreeNode(values[i])
            queue.append(current.left)
        i += 1
        if i < len(values) and values[i] is not None:
            current.right = TreeNode(values[i])
            queue.append(current.right)
        i += 1
    return root

def connect_to_db():
    try:
        connection = psycopg2.connect(
            user=os.environ.get("DATABASE_USER"),
            password=os.environ.get("DATABASE_PASSWORD"),
            host=os.environ.get("DATABASE_HOST"),
            port=os.environ.get("DATABASE_PORT"),
            database=os.environ.get("DATABASE_NAME")
        )
        cursor = connection.cursor()
        print("Connected to the database")
        cursor.close()
        connection.close()
    except Exception as error:
        print(f"Error connecting to database: {error}")

if __name__ == "__main__":
    connect_to_db()
    input_list = input("Enter the tree values in level order, separated by commas (use 'null' for None): ").strip()
    input_list = [val.strip() for val in input_list.split(',')]
    input_list = [int(val) if val.lower() != 'null' else None for val in input_list]
    root = buildTree(input_list)
    print("The maximum path sum is:", maxPathSum(root))
