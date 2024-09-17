
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Band, Venue, Concert

# Set up the SQLite database URL
DATABASE_URL = "sqlite:///./concerts.db"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session instance
session = Session()

# Create all tables
Base.metadata.create_all(engine)

def add_band(name, hometown):
    """Add a new band to the database."""
    band = Band(name=name, hometown=hometown)
    session.add(band)
    session.commit()
    return band

def add_venue(title, city):
    """Add a new venue to the database."""
    venue = Venue(title=title, city=city)
    session.add(venue)
    session.commit()
    return venue

def add_concert(band_id, venue_id, date):
    """Add a new concert to the database."""
    concert = Concert(band_id=band_id, venue_id=venue_id, date=date)
    session.add(concert)
    session.commit()
    return concert

def print_bands():
    """Print all bands."""
    print("Bands:")
    bands = session.query(Band).all()
    for band in bands:
        print(f"Band: {band.name}, Hometown: {band.hometown}")

def print_venues():
    """Print all venues."""
    print("Venues:")
    venues = session.query(Venue).all()
    for venue in venues:
        print(f"Venue: {venue.title}, City: {venue.city}")

def print_concerts():
    """Print all concerts."""
    print("Concerts:")
    concerts = session.query(Concert).all()
    for concert in concerts:
        band_name = concert.band.name if concert.band else "Unknown Band"
        venue_title = concert.venue.title if concert.venue else "Unknown Venue"
        print(f"Concert on {concert.date}: {band_name} at {venue_title}")

def example_usage():
    # Example usage: Adding data
    band = add_band("The Rockers", "New York")
    venue = add_venue("Madison Square Garden", "New York")
    concert = add_concert(band.id, venue.id, "2024-09-30")

    # Print data
    print_bands()
    print_venues()
    print_concerts()

    # Demonstrate the functionality of model methods
    band = session.query(Band).first()
    if band:
        print("Band Venues:", band.venues())
        print("Band Introductions:", band.all_introductions())
        print("Band with Most Performances:", Band.most_performances(session))

    venue = session.query(Venue).first()
    if venue:
        print("Venue Bands:", venue.bands())
        print("Concert on '2024-09-30' at Venue:", venue.concert_on("2024-09-30"))
        print("Most Frequent Band at Venue:", venue.most_frequent_band())

if __name__ == "__main__":
    example_usage()
