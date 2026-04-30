import heapq
from collections import deque
from datetime import datetime
import uuid

# ==================== LINKED LIST FOR ORDER HISTORY ====================

class OrderNode:
    """Node for customer order history linked list"""
    def __init__(self, order_id, items, total_amount, status):
        self.order_id = order_id
        self.items = items.copy()
        self.total_amount = total_amount
        self.status = status
        self.order_time = datetime.now()
        self.next = None

class OrderHistoryLinkedList:
    """Custom linked list for order history"""
    def __init__(self):
        self.head = None
        self.length = 0
    
    def add_order(self, order_id, items, total_amount, status):
        """Add order to beginning of list"""
        new_node = OrderNode(order_id, items, total_amount, status)
        new_node.next = self.head
        self.head = new_node
        self.length += 1
        return True
    
    def update_status(self, order_id, new_status):
        """Update order status"""
        current = self.head
        while current:
            if current.order_id == order_id:
                current.status = new_status
                return True
            current = current.next
        return False
    
    def get_recent_orders(self, count=5):
        """Get most recent orders"""
        result = []
        current = self.head
        while current and len(result) < count:
            result.append({
                'order_id': current.order_id,
                'total': current.total_amount,
                'status': current.status,
                'time': current.order_time.strftime("%H:%M")
            })
            current = current.next
        return result

# ==================== STACK FOR BILLS ====================

class BillStack:
    """Stack for recent bills (LIFO)"""
    def __init__(self):
        self.stack = []
    
    def push(self, bill):
        """Add bill to stack"""
        bill['time'] = datetime.now().strftime("%H:%M:%S")
        self.stack.append(bill)
    
    def get_last_bill(self):
        """Get most recent bill without removing"""
        if not self.stack:
            return None
        return self.stack[-1]
    
    def is_empty(self):
        return len(self.stack) == 0

# ==================== QUEUE FOR KITCHEN ORDERS ====================

class KitchenQueue:
    """FIFO queue for kitchen orders"""
    def __init__(self):
        self.queue = deque()
    
    def add_order(self, order_id, customer_name, items):
        """Add order to queue"""
        self.queue.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'items': items,
            'time': datetime.now().strftime("%H:%M:%S")
        })
        print(f"  📋 Order {order_id} added to kitchen queue")
    
    def get_next(self):
        """Get next order (FIFO)"""
        if not self.queue:
            return None
        return self.queue.popleft()
    
    def size(self):
        return len(self.queue)
    
    def view_all(self):
        return list(self.queue)

# ==================== PRIORITY QUEUE FOR VIP ORDERS ====================

class VIPQueue:
    """Priority queue for VIP customers"""
    def __init__(self):
        self.heap = []
        self.counter = 0
    
    def add_order(self, order_id, customer_name, items, priority):
        """Add VIP order (lower number = higher priority)"""
        heapq.heappush(self.heap, (priority, self.counter, order_id, customer_name, items))
        self.counter += 1
        priority_text = {1: "Platinum", 2: "Gold", 3: "Silver"}[priority]
        print(f"  👑 VIP Order {order_id} - {priority_text} priority")
    
    def get_next(self):
        """Get highest priority order"""
        if not self.heap:
            return None
        return heapq.heappop(self.heap)
    
    def size(self):
        return len(self.heap)

# ==================== TREE FOR MENU CATEGORIES ====================

class MenuCategory:
    """Node for menu category tree"""
    def __init__(self, name):
        self.name = name
        self.children = []
        self.items = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def add_item(self, item_id, name, price):
        self.items.append({'id': item_id, 'name': name, 'price': price})

class MenuTree:
    """Tree structure for menu organization"""
    def __init__(self):
        self.root = MenuCategory("Menu")
        self.next_id = 101
        self._build_menu()
    
    def _get_id(self):
        """Get next item ID"""
        self.next_id += 1
        return self.next_id
    
    def _build_menu(self):
        """Build menu hierarchy"""
        # Appetizers
        appetizers = MenuCategory("Appetizers")
        appetizers.add_item(self._get_id(), "Spring Rolls", 5.99)
        appetizers.add_item(self._get_id(), "Garlic Bread", 3.99)
        appetizers.add_item(self._get_id(), "Chicken Wings", 8.99)
        
        # Main Course
        main = MenuCategory("Main Course")
        
        # Subcategories under Main
        veg = MenuCategory("Vegetarian")
        veg.add_item(self._get_id(), "Veg Biryani", 12.99)
        veg.add_item(self._get_id(), "Paneer Butter Masala", 11.99)
        
        nonveg = MenuCategory("Non-Vegetarian")
        nonveg.add_item(self._get_id(), "Chicken Biryani", 14.99)
        nonveg.add_item(self._get_id(), "Butter Chicken", 15.99)
        nonveg.add_item(self._get_id(), "Fish Curry", 16.99)
        
        main.add_child(veg)
        main.add_child(nonveg)
        
        # Desserts
        desserts = MenuCategory("Desserts")
        desserts.add_item(self._get_id(), "Ice Cream", 3.99)
        desserts.add_item(self._get_id(), "Brownie", 4.99)
        desserts.add_item(self._get_id(), "Gulab Jamun", 4.49)
        
        # Beverages
        beverages = MenuCategory("Beverages")
        beverages.add_item(self._get_id(), "Soft Drink", 1.99)
        beverages.add_item(self._get_id(), "Fresh Juice", 3.49)
        beverages.add_item(self._get_id(), "Coffee", 2.99)
        
        # Add all to root
        self.root.add_child(appetizers)
        self.root.add_child(main)
        self.root.add_child(desserts)
        self.root.add_child(beverages)
    
    def display(self, node=None, level=0):
        """Display menu tree"""
        if node is None:
            node = self.root
            print("\n" + "="*50)
            print("  RESTAURANT MENU")
            print("="*50)
        
        indent = "  " * level
        if level > 0:
            print(f"{indent}📁 {node.name}")
        
        for item in node.items:
            print(f"{indent}  🍽️  {item['name']} - ${item['price']:.2f} (ID: {item['id']})")
        
        for child in node.children:
            self.display(child, level + 1)
    
    def get_item(self, item_id):
        """Get item by ID"""
        return self._search_item(self.root, item_id)
    
    def _search_item(self, node, item_id):
        """Recursive search"""
        for item in node.items:
            if item['id'] == item_id:
                return item
        for child in node.children:
            result = self._search_item(child, item_id)
            if result:
                return result
        return None
    
    def search_by_name(self, keyword):
        """Search items by name"""
        results = []
        self._search_name(self.root, keyword.lower(), results)
        return results
    
    def _search_name(self, node, keyword, results):
        """Recursive name search"""
        for item in node.items:
            if keyword in item['name'].lower():
                results.append(item)
        for child in node.children:
            self._search_name(child, keyword, results)

# ==================== POPULAR ITEMS TRACKER (ARRAY) ====================

class PopularItemsTracker:
    """Track popular items using dictionary and list"""
    def __init__(self):
        self.counts = {}
    
    def record(self, items):
        """Record items from order"""
        for item in items:
            item_id = item['id']
            if item_id in self.counts:
                self.counts[item_id] += 1
            else:
                self.counts[item_id] = 1
    
    def get_top(self, n=5, menu_tree=None):
        """Get top N popular items"""
        sorted_items = sorted(self.counts.items(), key=lambda x: x[1], reverse=True)
        top = sorted_items[:n]
        
        if top and menu_tree:
            print("\n  🔥 TOP 5 MOST POPULAR ITEMS 🔥")
            for i, (item_id, count) in enumerate(top, 1):
                item = menu_tree.get_item(item_id)
                if item:
                    print(f"  {i}. {item['name']} - Ordered {count} times")

# ==================== CUSTOMER CLASS ====================

class Customer:
    """Customer with order history (Hash Map key)"""
    def __init__(self, phone, name, vip_level=4):
        self.phone = phone
        self.name = name
        self.vip_level = vip_level  # 1=Platinum, 2=Gold, 3=Silver, 4=Regular
        self.history = OrderHistoryLinkedList()
        self.total_spent = 0
        self.visit_count = 0
    
    def add_order(self, order_id, items, total):
        """Add order to history"""
        self.history.add_order(order_id, items, total, "Preparing")
        self.total_spent += total
        self.visit_count += 1
    
    def update_order(self, order_id, status):
        """Update order status"""
        self.history.update_status(order_id, status)
    
    def get_vip_text(self):
        """Get VIP level text"""
        levels = {1: "Platinum 👑👑👑", 2: "Gold 👑👑", 3: "Silver 👑", 4: "Regular"}
        return levels.get(self.vip_level, "Regular")

# ==================== MAIN RESTAURANT SYSTEM ====================

class RestaurantSystem:
    def __init__(self):
        # Hash Maps
        self.customers = {}  # phone -> Customer
        self.active_orders = {}  # order_id -> order dict
        
        # Data structures
        self.menu = MenuTree()
        self.kitchen_queue = KitchenQueue()
        self.vip_queue = VIPQueue()
        self.bill_stack = BillStack()
        self.popular_tracker = PopularItemsTracker()
        
        # Arrays for statistics
        self.hourly_orders = [0] * 12  # 12 hours (11 AM to 10 PM)
        
        # Initialize sample data
        self._init_sample_data()
    
    def _init_sample_data(self):
        """Initialize sample customers"""
        # VIP customers
        self.register_customer("9876543210", "John Doe", 1)  # Platinum
        self.register_customer("8765432109", "Jane Smith", 2)  # Gold
        self.register_customer("7654321098", "Bob Johnson", 4)  # Regular
        
        print("\n✅ System ready with sample data!")
    
    # ========== HASH MAP OPERATIONS ==========
    def register_customer(self, phone, name, vip_level=4):
        """Register new customer"""
        if phone in self.customers:
            print(f"Customer {phone} already exists!")
            return False
        
        customer = Customer(phone, name, vip_level)
        self.customers[phone] = customer
        print(f"✅ Registered: {name} ({phone}) - {customer.get_vip_text()}")
        return True
    
    def get_customer(self, phone):
        """O(1) customer lookup"""
        return self.customers.get(phone)
    
    # ========== ORDER CREATION ==========
    def create_order(self, phone, item_ids, order_type="Dine-in"):
        """Create new order"""
        customer = self.get_customer(phone)
        if not customer:
            print(f"Customer {phone} not found! Please register first.")
            return None
        
        # Get items from menu
        items = []
        total = 0
        for item_id in item_ids:
            item = self.menu.get_item(item_id)
            if item:
                items.append(item)
                total += item['price']
            else:
                print(f"Warning: Item ID {item_id} not found")
        
        if not items:
            print("No valid items in order!")
            return None
        
        # Calculate total with tax
        tax = total * 0.10
        grand_total = total + tax
        
        # Create order
        order_id = str(uuid.uuid4())[:8]
        
        order = {
            'id': order_id,
            'customer_phone': phone,
            'customer_name': customer.name,
            'items': items,
            'subtotal': total,
            'tax': tax,
            'total': grand_total,
            'type': order_type,
            'status': 'Received'
        }
        
        self.active_orders[order_id] = order
        
        # Add to customer history
        customer.add_order(order_id, items, grand_total)
        
        # Record for popular items
        self.popular_tracker.record(items)
        
        # Update hourly stats
        hour = (datetime.now().hour - 11) % 12  # 11 AM = index 0
        if 0 <= hour < 12:
            self.hourly_orders[hour] += 1
        
        # Send to appropriate queue
        if customer.vip_level <= 2:
            self.vip_queue.add_order(order_id, customer.name, items, customer.vip_level)
        else:
            self.kitchen_queue.add_order(order_id, customer.name, items)
        
        print(f"\n✅ ORDER CREATED: {order_id}")
        print(f"   Customer: {customer.name}")
        print(f"   Items: {len(items)} items")
        print(f"   Total: ${grand_total:.2f}")
        
        return order_id
    
    # ========== ORDER PROCESSING ==========
    def process_order(self):
        """Process next order (priority to VIP)"""
        # Check VIP queue first
        if not self.vip_queue.size() == 0:
            vip_order = self.vip_queue.get_next()
            if vip_order:
                priority, counter, order_id, customer_name, items = vip_order
                print(f"\n👑 PROCESSING VIP ORDER: {order_id}")
                print(f"   Customer: {customer_name}")
                
                if order_id in self.active_orders:
                    self.active_orders[order_id]['status'] = 'Preparing'
                    customer = self.get_customer(self.active_orders[order_id]['customer_phone'])
                    if customer:
                        customer.update_order(order_id, 'Preparing')
                return order_id
        
        # Check regular queue
        if not self.kitchen_queue.size() == 0:
            order = self.kitchen_queue.get_next()
            if order:
                print(f"\n📋 PROCESSING ORDER: {order['order_id']}")
                print(f"   Customer: {order['customer_name']}")
                
                if order['order_id'] in self.active_orders:
                    self.active_orders[order['order_id']]['status'] = 'Preparing'
                    customer = self.get_customer(self.active_orders[order['order_id']]['customer_phone'])
                    if customer:
                        customer.update_order(order['order_id'], 'Preparing')
                return order['order_id']
        
        print("\nNo orders in queue")
        return None
    
    # ========== ORDER COMPLETION ==========
    def complete_order(self, order_id):
        """Complete order and generate bill"""
        if order_id not in self.active_orders:
            print("Order not found!")
            return None
        
        order = self.active_orders[order_id]
        order['status'] = 'Completed'
        
        # Update customer history
        customer = self.get_customer(order['customer_phone'])
        if customer:
            customer.update_order(order_id, 'Completed')
        
        # Create bill
        bill = {
            'order_id': order_id,
            'customer': order['customer_name'],
            'subtotal': order['subtotal'],
            'tax': order['tax'],
            'total': order['total']
        }
        
        # Push to stack
        self.bill_stack.push(bill)
        
        print(f"\n✅ ORDER COMPLETED: {order_id}")
        self.print_bill(order_id)
        
        return bill
    
    def print_bill(self, order_id):
        """Print bill for order"""
        if order_id not in self.active_orders:
            return
        
        order = self.active_orders[order_id]
        
        print("\n" + "="*55)
        print("  RESTAURANT BILL".center(55))
        print("="*55)
        print(f"Order ID: {order['id']}")
        print(f"Customer: {order['customer_name']}")
        print(f"Type: {order['type']}")
        print("-"*55)
        print(f"{'Item':<35} {'Price':>10}")
        print("-"*55)
        
        for item in order['items']:
            print(f"{item['name']:<35} ${item['price']:>9.2f}")
        
        print("-"*55)
        print(f"{'Subtotal':<35} ${order['subtotal']:>9.2f}")
        print(f"{'Tax (10%)':<35} ${order['tax']:>9.2f}")
        print(f"{'TOTAL':<35} ${order['total']:>9.2f}")
        print("="*55)
        print("  Thank you for dining with us!".center(55))
        print("="*55)
    
    def reprint_bill(self):
        """Reprint last bill from stack"""
        last = self.bill_stack.get_last_bill()
        if last:
            print("\n" + "="*55)
            print("  REPRINT - LAST BILL".center(55))
            print("="*55)
            print(f"Order ID: {last['order_id']}")
            print(f"Customer: {last['customer']}")
            print(f"Total: ${last['total']:.2f}")
            print(f"Time: {last['time']}")
            print("="*55)
        else:
            print("No bills to reprint")
    
    # ========== VIEW FUNCTIONS ==========
    def view_menu(self):
        """Display menu tree"""
        self.menu.display()
    
    def view_queues(self):
        """View queue status"""
        print("\n" + "="*50)
        print("  QUEUE STATUS".center(50))
        print("="*50)
        
        print(f"\n👑 VIP Queue: {self.vip_queue.size()} orders waiting")
        print(f"📋 Regular Queue: {self.kitchen_queue.size()} orders waiting")
        
        # Show regular queue details
        if self.kitchen_queue.size() > 0:
            print("\nRegular Queue Orders:")
            for order in self.kitchen_queue.view_all():
                print(f"  • {order['order_id']} - {order['customer_name']}")
    
    def view_customer_history(self, phone):
        """View customer order history (Linked List)"""
        customer = self.get_customer(phone)
        if not customer:
            print("Customer not found!")
            return
        
        print(f"\n{'='*50}")
        print(f"  CUSTOMER: {customer.name}".center(50))
        print(f"{'='*50}")
        print(f"Phone: {customer.phone}")
        print(f"VIP Status: {customer.get_vip_text()}")
        print(f"Total Visits: {customer.visit_count}")
        print(f"Total Spent: ${customer.total_spent:.2f}")
        print("-"*50)
        
        orders = customer.history.get_recent_orders(5)
        if not orders:
            print("No orders yet")
        else:
            print("Recent Orders:")
            for order in orders:
                print(f"  {order['time']} - {order['order_id']} - ${order['total']:.2f} - {order['status']}")
    
    def view_statistics(self):
        """Display statistics (Arrays + Popular items)"""
        print("\n" + "="*50)
        print("  RESTAURANT STATISTICS".center(50))
        print("="*50)
        
        # Popular items
        self.popular_tracker.get_top(5, self.menu)
        
        # Hourly distribution
        print("\n📊 HOURLY ORDER DISTRIBUTION:")
        hours = ["11AM", "12PM", "1PM", "2PM", "3PM", "4PM", "5PM", "6PM", "7PM", "8PM", "9PM", "10PM"]
        for i, count in enumerate(self.hourly_orders):
            if count > 0:
                print(f"  {hours[i]}: {count} orders")
        
        # Active orders
        active = [o for o in self.active_orders.values() if o['status'] != 'Completed']
        print(f"\n🔄 Active Orders: {len(active)}")
    
    def search_menu(self):
        """Search menu items"""
        keyword = input("Enter item name to search: ")
        results = self.menu.search_by_name(keyword)
        
        if results:
            print(f"\nFound {len(results)} items:")
            for item in results:
                print(f"  🍽️  {item['name']} - ${item['price']:.2f}")
        else:
            print("No items found")
    
    # ========== MENU INTERFACE ==========
    def run(self):
        """Main menu loop"""
        while True:
            print("\n" + "="*55)
            print("  RESTAURANT MANAGEMENT SYSTEM".center(55))
            print("="*55)
            print("1. View Menu (Tree Structure)")
            print("2. Register Customer (Hash Map)")
            print("3. Create Order")
            print("4. Process Next Order (Queue/Priority)")
            print("5. Complete Order & Bill")
            print("6. View Kitchen Queues")
            print("7. Customer History (Linked List)")
            print("8. Reprint Last Bill (Stack)")
            print("9. View Statistics (Arrays)")
            print("10. Search Menu")
            print("11. Exit")
            print("="*55)
            
            choice = input("\nEnter choice (1-11): ")
            
            if choice == '1':
                self.view_menu()
            
            elif choice == '2':
                print("\n--- REGISTER CUSTOMER ---")
                phone = input("Phone number: ")
                name = input("Name: ")
                print("\nVIP Levels:")
                print("1 - Platinum (Highest priority)")
                print("2 - Gold")
                print("3 - Silver")
                print("4 - Regular")
                try:
                    vip = int(input("Enter level (1-4): "))
                    if vip not in [1,2,3,4]:
                        vip = 4
                except:
                    vip = 4
                self.register_customer(phone, name, vip)
            
            elif choice == '3':
                print("\n--- CREATE ORDER ---")
                self.view_menu()
                phone = input("\nCustomer phone: ")
                
                # Auto-register if new
                if phone not in self.customers:
                    print("New customer! Quick registration:")
                    name = input("Enter name: ")
                    self.register_customer(phone, name, 4)
                
                items_input = input("Enter item IDs (comma-separated, e.g., 101,102): ")
                try:
                    item_ids = [int(x.strip()) for x in items_input.split(',')]
                except:
                    print("Invalid input!")
                    continue
                
                print("\nOrder type:")
                print("1 - Dine-in")
                print("2 - Takeaway")
                type_choice = input("Choice: ")
                order_type = "Dine-in" if type_choice == "1" else "Takeaway"
                
                self.create_order(phone, item_ids, order_type)
            
            elif choice == '4':
                self.process_order()
            
            elif choice == '5':
                order_id = input("Enter Order ID to complete: ")
                self.complete_order(order_id)
            
            elif choice == '6':
                self.view_queues()
            
            elif choice == '7':
                phone = input("Enter customer phone: ")
                self.view_customer_history(phone)
            
            elif choice == '8':
                self.reprint_bill()
            
            elif choice == '9':
                self.view_statistics()
            
            elif choice == '10':
                self.search_menu()
            
            elif choice == '11':
                print("\n👋 Thank you for using Restaurant Management System!")
                break
            
            else:
                print("Invalid choice!")
            
            input("\nPress Enter to continue...")

# ==================== RUN ====================
if __name__ == "__main__":
    print("="*55)
    print("  WELCOME TO RESTAURANT MANAGEMENT".center(55))
    print("="*55)
    print("\nInitializing system...")
    
    try:
        system = RestaurantSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\nProgram stopped by user")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please restart the program")
