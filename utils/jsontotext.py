import json

def json_to_text(json_file, output_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    count = 0
    with open(output_file, 'w') as f:
        # Loop over each community in the array
        for community in data:
            # Extract and write community information
            try:
                f.write(f"Community Name: {community['community_name']}\n")
                f.write(f"Details Link: {community['details_link']}\n")
                f.write(f"Badge: {community['badge']}\n")
                f.write(f"Status: {community['status']}\n")
                f.write(f"Price: {community['price']}\n")
                f.write(f"Address: {community['address']}\n")
                f.write(f"Overview: {community['overview']}\n\n")
                
                # Homes information
                f.write("Homes:\n")
                for home in community['homes']:
                    f.write(f"  Site ID: {home['site_id']}\n")
                    f.write(f"  Price: {home['price']}\n")
                    f.write(f"  Plan: {home['plan']}\n")
                    f.write(f"  Home Details: {home['home_details']}\n")
                    f.write(f"  Address: {home['address']}\n")
                    f.write(f"  Details Link: {home['details_link']}\n")
                    
                    # Homesite details
                    site_info = home['site_info']
                    f.write(f"  Homesite Status: {site_info['homesite_status']}\n")
                    f.write(f"  Homesite Price: {site_info['price']}\n")
                    f.write(f"  Homesite Details: {site_info['homesite_details']}\n")
                    f.write(f"  Homesite Address: {site_info['address']}\n")
                    f.write(f"  Contact Number: {site_info['contact_number']}\n")
                    
                    # Links
                    f.write("  Links:\n")
                    for link in site_info['links']:
                        f.write(f"    - {link}\n")
                    
                    # Schools
                    f.write("  Schools:\n")
                    for school in site_info['schools']:
                        f.write(f"    School Name: {school['school_name']}\n")
                        f.write(f"    Grade: {school['school_grade']}\n")
                        f.write(f"    District: {school['school_district']}\n")
                        f.write(f"    Rating: {school['school_rating']}\n")
                        f.write(f"    Niche Link: {school['niche_link']}\n")

                    # Nearby places
                    f.write("  Nearby Places:\n")
                    for place in site_info['nearby_places']:
                        f.write(f"    Name: {place['name']}\n")
                        f.write(f"    Details: {place['details']}\n")
                        f.write(f"    Rating: {place['rating']}\n")
                        f.write(f"    Reviews: {place['reviews']}\n")
                    
                    f.write("\n")
                
                # Amenities information
                f.write("Amenities:\n")
                for amenity in community['amenities']:
                    f.write(f"  Name: {amenity['name']}\n")
                    f.write(f"  Details: {amenity['details']}\n")
                
                # Nearby places information
                f.write("\nNearby Places:\n")
                for place in community['nearby_places']:
                    f.write(f"  Name: {place['name']}\n")
                    f.write(f"  Details: {place['details']}\n")
                    f.write(f"  Rating: {place['rating']}\n")
                    f.write(f"  Reviews: {place['reviews']}\n")

                f.write("\n" + "="*80 + "\n\n")  # Separator between communities
                count += 1
            except Exception as e:
                print(f"Error processing community {community['community_name']}: {e}")
            
        print(f"Processed {count} communities")
# Usage
# json_to_text('communities_data.json', 'communities_data.txt')
