import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
import userbackend
from math import radians, sin, cos, sqrt, atan2



class TomTomStaticMap:
    def __init__(self, api_key, place_name):
        self.api_key = api_key
        self.place_name = place_name

        # Use the Search API to get coordinates for the specified place
        coordinates = self.get_coordinates()
        self.latitude, self.longitude = coordinates

        # Default zoom level
        self.zoom_level = 15

        # TomTom Static Maps API endpoint with reduced size
        self.endpoint = f"https://api.tomtom.com/map/1/staticimage?key={self.api_key}&center={self.longitude},{self.latitude}&zoom={self.zoom_level}&size=700x300"

        # Make a request to TomTom API
        response = requests.get(self.endpoint)

        self.map_image = Image.open(BytesIO(response.content))
        self.map_image = self.map_image.resize((650, 200))
        self.map_photo = ImageTk.PhotoImage(self.map_image)
    
    def get_coordinates(self):
        # Use TomTom Search API to get coordinates for the specified place
        search_endpoint = f"https://api.tomtom.com/search/2/search/{self.place_name}.json?key={self.api_key}"
        response = requests.get(search_endpoint)
        data = response.json()

        # Extract the coordinates from the search results
        if data.get("results") and data["results"][0].get("position"):
            coordinates = data["results"][0]["position"]
            return coordinates["lat"], coordinates["lon"]
        else:
            raise ValueError(f"Could not find coordinates for the place: {self.place_name}")

    


class App:
    def __init__(self, root,connection):
        # Setting title
        self.connection = connection
        self.user_id_entry1 = None
        userbackend.create_user_registration_table(self.connection)
        root.title("Delivery Management")
        root.geometry("1220x1000")
        root.resizable(width=False, height=False)

        # Create three frames
        frame1 = tk.Frame(root, bg="black", height=1000, width=200)
        frame2 = tk.Frame(root, bg="white", height=1000, width=800)
        frame3 = tk.Frame(root, bg="black", height=1000, width=200)

        # Pack the frames horizontally
        frame1.pack(side=tk.LEFT, fill=tk.Y)
        frame2.pack(side=tk.LEFT, fill=tk.Y)
        frame3.pack(side=tk.LEFT, fill=tk.Y)


        form_frame = ttk.Frame(frame1)
        form_frame.place(x=20, y=20, width=170, height=300)

        title_label = ttk.Label(form_frame, text="User Registration", font=("Arial", 13, "bold"))
        title_label.place(x=20, y=15)




#   forms in frame 1
     
    #  user registration form

        name_label = ttk.Label(form_frame, text="Name:")
        name_label.place(x=20, y=40)
        
        name_entry1 = ttk.Entry(form_frame, width=20)
        name_entry1.place(x=20, y=60)

        email_label = ttk.Label(form_frame, text="Email:")
        email_label.place(x=20, y=85)

        email_entry = ttk.Entry(form_frame, width=20)
        email_entry.place(x=20, y=105)

        phone_number_label = ttk.Label(form_frame, text="Phone Number:")
        phone_number_label.place(x=20, y=130)

        phone_number_entry = ttk.Entry(form_frame, width=20)
        phone_number_entry.place(x=20, y=150)

        user_id_label = ttk.Label(form_frame, text="User Id:")
        user_id_label.place(x=20, y=175)

        user_id = ttk.Entry(form_frame, width=20)
        user_id.place(x=20, y=195)


        password_label = ttk.Label(form_frame, text="Password:")
        password_label.place(x=20, y=220)

        password_entry = ttk.Entry(form_frame, width=20, show="*")  # show="*" hides the entered text
        password_entry.place(x=20, y=240)
    

        submit_button = ttk.Button(form_frame, text="Submit",command=lambda: self.submit_form(name_entry1.get(), email_entry.get(), phone_number_entry.get(), user_id.get(), password_entry.get()))
        submit_button.place(x=20, y=270)





    # Update registration form
        
        update_frame = ttk.Frame(frame1)
        update_frame.place(x=20, y=350, width=170, height=250)


        update_label = ttk.Label(update_frame, text="Update Registration", font=("Arial", 11, "bold"))
        update_label.place(x=20, y=10)

        user_id_entry1label = ttk.Label(update_frame, text="User Id")
        user_id_entry1label.place(x=20, y=40)

        self.user_id_entry1 = ttk.Entry(update_frame, width=20)
        self.user_id_entry1.place(x=20, y=60)

        new_password_label = ttk.Label(update_frame, text="New Password:")
        new_password_label.place(x=20, y=85)

        self.new_password_entry = ttk.Entry(update_frame, width=20, show="*")
        self.new_password_entry.place(x=20, y=105)

        confirm_password_label = ttk.Label(update_frame, text="Confirm New Password:")
        confirm_password_label.place(x=20, y=130)

        self.confirm_password_entry = ttk.Entry(update_frame, width=20, show="*")
        self.confirm_password_entry.place(x=20, y=150)


        update_submit_button = ttk.Button(update_frame, text="Update", command=lambda: self.update_registration())
        update_submit_button.place(x=20, y=180)











    #  Elements in frame 2

       
    #    Map

        # TomTom API Key (replace with your actual API key)
        self.api_key = '6fUbXjdwGZT5Y7ZGxDdpp3nGLlsi1XvB'  # Replace with your actual TomTom API key
        self.place_name = 'KIIT'  # Replace with the desired place name
        self.tom_tom_map = TomTomStaticMap(self.api_key, self.place_name)

        # Display the map in a Tkinter Label
        self.map_image = self.tom_tom_map.map_image
        self.map_photo = self.tom_tom_map.map_photo
        self.map_label = tk.Label(frame2, image=self.map_photo)
        self.map_label.image = self.map_photo  # Keep a reference to the image
        self.map_label.place(x=30, y=50, anchor="nw")   # Place the map at the top-left corner

        title_label = ttk.Label(frame2, text="Active Shipment", font=("Arial", 14, "bold"), foreground="white", background="black")
        title_label.place(x=20, y=10, anchor="nw")

        # Bind mouse click events for zooming
        self.map_label.bind("<Button-1>", self.zoom_in)  # Left mouse click for zoom in
        self.map_label.bind("<Button-3>", self.zoom_out)  # Right mouse click for zoom out






        # delivery form

        title_label = ttk.Label(frame2, text="Delivery Form", font=("Arial", 18, "bold"))
        title_label.place(x=20, y=260, anchor="nw")
 
# Add space between the title and the rest of the form
        separator = ttk.Separator(frame2, orient="horizontal")  
        separator.place(x=20, y=50, width=600)

        destination_id_label = ttk.Label(frame2, text="Destination ID:")
        destination_id_label.place(x=20, y=300)

        self.destination_id = ttk.Entry(frame2, width=30)
        self.destination_id.place(x=20, y=320)

# Create a label and entry field for Name
        name_label = ttk.Label(frame2, text="Name:")
        name_label.place(x=20, y=345)

        self.name_entry = ttk.Entry(frame2, width=30)
        self.name_entry.place(x=20, y=365)

# Create a label and entry field for Latitude
        latitude_label = ttk.Label(frame2, text="Street:")
        latitude_label.place(x=20, y=390)

        self.latitude_entry1 = ttk.Entry(frame2, width=30)
        self.latitude_entry1.place(x=20, y=410)

# Create a label and entry field for Longitude
        longitude_label = ttk.Label(frame2, text="City")
        longitude_label.place(x=20, y=435)

        self.longitude_entry1 = ttk.Entry(frame2, width=30)
        self.longitude_entry1.place(x=20, y=455)

# Create a label and entry field for Address
        address_label = ttk.Label(frame2, text="State")
        address_label.place(x=20, y=480)
        
        self.address_entry = ttk.Entry(frame2, width=35)
        self.address_entry.place(x=20, y=500)

# Create a submit button
        submit_button = ttk.Button(frame2, text="Submit Delivery", command=self.submit_delivery)
        submit_button.place(x=20, y=530)







        # address form

        
        # address form
        address_form_label = ttk.Label(frame2, text="Address Form", font=("Arial", 18, "bold"))
        address_form_label.place(x=430, y=295, anchor="se")

        separator_address_form = ttk.Separator(frame2, orient="horizontal")
        separator_address_form.place(x=50, y=50, width=600)

        latitude_label = ttk.Label(frame2, text="Room/ Flat No.")
        latitude_label.place(x=270, y=300)  # Adjusted placement

        self.latitude_entry = ttk.Entry(frame2, width=30)
        self.latitude_entry.place(x=270, y=320)

        longitude_label = ttk.Label(frame2, text="Floor")
        longitude_label.place(x=270, y=345)

        self.longitude_entry = ttk.Entry(frame2, width=30)
        self.longitude_entry.place(x=270, y=365)

        street_label = ttk.Label(frame2, text="Street:")
        street_label.place(x=270, y=390)

        self.street_entry = ttk.Entry(frame2, width=30)
        self.street_entry.place(x=270, y=410)

        city_label = ttk.Label(frame2, text="City:")
        city_label.place(x=270, y=435)

        self.city_entry = ttk.Entry(frame2, width=30)
        self.city_entry.place(x=270, y=455)

        state_label = ttk.Label(frame2, text="State:")
        state_label.place(x=270, y=480)

        self.state_entry = ttk.Entry(frame2, width=30)
        self.state_entry.place(x=270, y=500)

        phn_label = ttk.Label(frame2, text="Phone No:")
        phn_label.place(x=270, y=525)

        self.phn_entry = ttk.Entry(frame2, width=30)
        self.phn_entry.place(x=270, y=545)

# Create a submit button for the address form
        submit_address_button = ttk.Button(frame2, text="Submit Address", command=self.submit_address)
        submit_address_button.place(x=270, y=580)



        profile_frame = tk.Frame(frame3, bg="black", padx=10, pady=10)
        profile_frame.pack(pady=(10, 0))  

# Title for the Profile Frame
        title_label = ttk.Label(profile_frame, text="Profile", font=("Arial", 10, "bold"), foreground="white", background="black")
        title_label.pack()

# Display "Alex Benjamin"
        name_label = tk.Label(profile_frame, text="Alex", font=("Arial", 14), background="black", foreground="white", padx=5, pady=2)
        name_label.pack()

# Information about packages
        info_label = tk.Label(profile_frame, text="10 packages 0rdered   |   20 packages Delivered", font=("Arial", 7), background="black", foreground="white", padx=5, pady=2)
        info_label.pack()

# Additional information within the main box if needed
        additional_info_label = tk.Label(profile_frame, text="Additional Information", font=("Arial", 12, "bold"), background="black", foreground="white", padx=5, pady=2)
        additional_info_label.pack()


        # Assuming you have a frame3 created earlier
        address_frame = tk.Frame(frame3, bg="black", padx=10, pady=10)
        address_frame.pack(pady=(10, 0))  # Add some padding at the top

# Title for the Address Frame
       # Title for the Address Frame
        address_title_label = ttk.Label(address_frame, text="Saved Addresses", font=("Arial", 16, "bold"), foreground="white", background="black")
        address_title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Display saved addresses using a Text widget with checkboxes
        self.saved_addresses_text = tk.Text(address_frame, height=23, width=20, font=("Arial", 11), background="white", foreground="black")
        self.saved_addresses_text.config(state=tk.NORMAL)
        self.saved_addresses_text.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        fetch_addresses_button = ttk.Button(address_frame, text="Fetch Addresses", command=self.display_addresses)
        fetch_addresses_button.grid(row=2, column=0, pady=(0, 10))

        # Add a button to get selected addresses
        get_selected_button = ttk.Button(address_frame, text="Select Addresses", command=self.get_selected_addresses)
        get_selected_button.grid(row=2, column=1, pady=(0, 10))

        self.address_checkboxes = []  # List to store Checkbuttons
        self.addresses = []

    def fetch_delivery_addresses_from_database(self):
    # Fetch addresses from the delivery_registration table
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT street, city, state FROM delivery_registration")
            addresses = cursor.fetchall()
            cursor.close()
            return addresses
        except Exception as e:
            return []

        
    def get_coordinates(self, street, city, state):
        # Use TomTom Search API to get coordinates for the specified place
        place_name = f"{street}, {city}, {state}"
        search_endpoint = f"https://api.tomtom.com/search/2/search/{place_name}.json?key={self.api_key}"
        response = requests.get(search_endpoint)
        data = response.json()

        # Extract the coordinates from the search results
        if data.get("results") and data["results"][0].get("position"):
            coordinates = data["results"][0]["position"]
            return coordinates["lat"], coordinates["lon"]
        else:
            raise ValueError(f"Could not find coordinates for the place: {place_name}")
 

    def display_addresses(self):
    # Clear the existing content in the Text widget
        self.saved_addresses_text.config(state=tk.NORMAL)
        self.saved_addresses_text.delete("1.0", tk.END)

    # Fetch and display addresses from the database
        self.addresses = self.fetch_addresses_from_database()
        for i, address in enumerate(self.addresses):
            checkbox_var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(self.saved_addresses_text, variable=checkbox_var)
            checkbox.grid(row=i, column=0, sticky=tk.W)
            self.address_checkboxes.append(checkbox)

            # Insert address details next to the checkbox
            self.saved_addresses_text.window_create(tk.END, window=checkbox)
            self.saved_addresses_text.insert(tk.END, f" {address['street']}, {address['city']}, {address['state']},\n")
            

    # Make the Text widget read-only
        self.saved_addresses_text.config(state=tk.DISABLED)
        

    def fetch_addresses_from_database(self):
        # Fetch addresses from the database
        try:
                cursor = self.connection.cursor(dictionary=True)
                cursor.execute("SELECT street, city, state, phn FROM address_book")
                addresses = cursor.fetchall()
                cursor.close()
                return addresses
        except Exception as e:
                return []

    def select_text(self, event):
        # Get the selected text
        selected_index = self.saved_addresses_text.index(tk.SEL_FIRST)
        selected_line = int(selected_index.split('.')[0]) - 1  

        # Perform some action with the selected text (e.g., print it)
        if 0 <= selected_line < len(self.addresses):
            selected_address = self.addresses[selected_line]
            print("Selected Address:")
            print(selected_address)

        # Disable further text selection
        self.saved_addresses_text.tag_remove(tk.SEL, "1.0", tk.END)
    
    def haversine_distance(self, coord1, coord2):
        lon1, lat1 = coord1
        lon2, lat2 = coord2

        R = 6371  # Earth radius in kilometers
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)

        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance

    def get_selected_addresses(self):
    # Get selected addresses based on checkboxes in the user addresses
        selected_user_addresses = [(address['street'], address['city'], address['state']) for address, checkbox in zip(self.addresses, self.address_checkboxes) if checkbox.instate(['selected'])]

        print("Selected User Addresses:")
        selected_user_coordinates = {}

        for street, city, state in selected_user_addresses:
            print(f"Street: {street}, City: {city}, State: {state}")

            try:
            # Get coordinates for the selected user address
                latitude, longitude = self.get_coordinates(street, city, state)
                print(f"Coordinates for {street}, {city}, {state}: Latitude: {latitude}, Longitude: {longitude}")
                selected_user_coordinates[(street, city, state)] = (latitude, longitude)

            except ValueError as e:
                print(f"Error getting coordinates: {e}")

    # Fetch delivery addresses from the database
        delivery_addresses = self.fetch_delivery_addresses_from_database()

        print("\nSelected Delivery Addresses:")
        selected_delivery_coordinates = {}

        for address in delivery_addresses:
            street, city, state = address['street'], address['city'], address['state']
            print(f"Street: {street}, City: {city}, State: {state}")

            try:
            # Get coordinates for the selected delivery address
                latitude, longitude = self.get_coordinates(street, city, state)
                print(f"Coordinates for {street}, {city}, {state}: Latitude: {latitude}, Longitude: {longitude}")
                selected_delivery_coordinates[(street, city, state)] = (latitude, longitude)

            except ValueError as e:
                print(f"Error getting coordinates: {e}")

    # Now you have separate coordinates for user and delivery addresses
        print("\nGraph:")
        graph = {}

        for source, source_coord in selected_user_coordinates.items():
            graph[source] = {}
            for destination, destination_coord in selected_delivery_coordinates.items():
            # Calculate distance between source (user) and destination (delivery) coordinates
                distance = self.haversine_distance(source_coord, destination_coord)
                graph[source][destination] = distance
                print(f"Distance from {source} to {destination}: {distance:.3f} km")



        

    # functions for frame 1
    def submit_form(self, name, email, phone_number, user_id, password):
        name_entry_value=name
        email_entry=email
        phone_number_entry=phone_number
        user_id_entry=user_id
        password_entry=password
        
        
        userbackend.insert_user_data(self.connection, name_entry_value, email_entry, phone_number_entry, user_id_entry, password_entry)

    
 
    def update_registration(self):
        current_password=self.user_id_entry1.get()
        new_password=self.new_password_entry.get()
        confirm_password=self.confirm_password_entry.get()
        
        userbackend.update_user_data(self.connection,current_password,new_password,confirm_password)


    

    
# functions for frame 2 
    def submit_address(self):
        latitude=self.latitude_entry.get()
        longitude =self.longitude_entry.get()
        street = self.street_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        phn = self.phn_entry.get()
        userbackend.add_address(self.connection,latitude,longitude,street,city,state,phn)


        

    def zoom_in(self, event):
        # Respond to left mouse click to zoom in
        self.zoom_level += 1
        self.update_map()

    def zoom_out(self, event):
        # Respond to right mouse click to zoom out
        self.zoom_level -= 1
        if self.zoom_level < 1:
            self.zoom_level = 1
        self.update_map()

    def update_map(self):
        # Update the map image with the new zoom level
        self.endpoint = f"https://api.tomtom.com/map/1/staticimage?key={self.api_key}&center={self.longitude},{self.latitude}&zoom={self.zoom_level}&size=700x300"
        response = requests.get(self.endpoint)
        self.map_image = Image.open(BytesIO(response.content))
        self.map_image = self.map_image.resize((600, 200))
        self.map_photo = ImageTk.PhotoImage(self.map_image)

        # Update the map label
        self.map_label.config(image=self.map_photo)
        self.map_label.image = self.map_photo

    
    def submit_delivery(self):
        destination_id1 = self.destination_id.get()
        name1 = self.name_entry.get()
        latitude = self.latitude_entry1.get()
        longitude = self.longitude_entry1.get()
        address1 = self.address_entry.get()

        userbackend.insert_delivery_data(self.connection, destination_id1, name1, latitude, longitude, address1)

#         latitude_longitude_list = self.fetch_all_latitude_longitude()

#         # Now latitude_longitude_list contains a list of tuples with latitude and longitude pairs       
#         for latitude, longitude in latitude_longitude_list:
#                 print(f"Latitude: {latitude}, Longitude: {longitude}")

#     def fetch_all_latitude_longitude(self):
#         select_query = """
#         SELECT latitude, longitude FROM delivery_registration
#         """
#         with connection.cursor() as cursor:
#                 cursor.execute(select_query)
#                 results = cursor.fetchall()
#                 latitude_longitude_list = [(result['latitude'], result['longitude']) for result in results]
#                 return latitude_longitude_list



if __name__ == "__main__":
    
    root = tk.Tk()
    db_connection = userbackend.connect_to_database()
    app = App(root, db_connection)
    root.mainloop()
