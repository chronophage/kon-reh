def get_unicode_card(suit, rank):
    """Get Unicode representation of a card"""
    suit_symbols = {
        "Hearts": "♥",
        "Diamonds": "♦",
        "Clubs": "♣",
        "Spades": "♠"
    }
    
    rank_display = {
        "Jack": "J",
        "Queen": "Q",
        "King": "K",
        "Ace": "A"
    }
    
    suit_symbol = suit_symbols.get(suit, "?")
    rank_symbol = rank_display.get(str(rank), str(rank))
    
    return f"{rank_symbol}{suit_symbol}"
