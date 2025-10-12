def _create_fleet(self):
        """Create a fleet of aliens"""
        alien = Alien(self)
        self.aliens.add(alien)