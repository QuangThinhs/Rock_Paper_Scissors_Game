class GameLogic:
    @staticmethod
    def determine_winner(choice1, choice2):
        """Xác định người chiến thắng"""
        if choice1 == choice2:
            return 'draw'
        wins = {
            'rock': 'scissors',
            'paper': 'rock',
            'scissors': 'paper'
        }
        return 'player1' if wins.get(choice1) == choice2 else 'player2'
    
    @staticmethod
    def get_choice_emoji(choice):
        """Lấy emoji tương ứng với lựa chọn"""
        emojis = {
            'rock': '✊',
            'paper': '✋',
            'scissors': '✌️'
        }
        return emojis.get(choice, '❓')