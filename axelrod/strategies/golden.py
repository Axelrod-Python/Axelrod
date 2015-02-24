from Axelrod import Player

class Golden(Player)
    """The player will always aim to bring the ratio of co-operations to defections closer to the golden mean"""
    
    name = 'Golden'
    gmean = 1.618
    
    def strategy(self,opponent):
        
        """initially co-operates"""
        if len(opponent.history) == 0:
            return 'C'
            
        """to avoid initial division by zero"""
        if sum([s == 'D' for s in opponent.history]) == 0:
            return 'D'
            
        """otherwise compare ratio to golden mean"""
        if (sum([p == 'C' for p in opponent.history]) + sum([q == 'C' for q in self.history]))/(sum([x == 'D' for x in opponent.history]) + sum([y == 'D' for y in self.history])) > gmean:
            return 'D'
        return 'C'
        
            
        
    
    
    
    
