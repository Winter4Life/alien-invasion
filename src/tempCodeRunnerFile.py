def _ship_hit(self):
        """Responds to the ship being hit"""
        # Decrement ships_left
        self.stats.ships_left -= 1
        
        # Delete remaining bullets and recreate fleet and ship
        self.bullets.empty()
        self.aliens.empty()
        self._create_fleet()
        self.ship.center_ship()