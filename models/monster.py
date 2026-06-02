from typing import Dict, Any
from utils.dice_parser import parse_hit_dice


class Monster:
    """Represents a D&D monster with its attributes.
    
    This class validates required fields and computes derived attributes
    eagerly during initialization for better performance and reliability.
    """
    
    def __init__(self, data: Dict[str, Any]):
        """Initialize a Monster from API response data.
        
        Validates required fields and computes derived attributes immediately.
        This ensures fast property access and fail-fast error handling.
        
        Args:
            data: Dictionary containing monster data from the API
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        self._data = data
        
        # Basic attributes (with defaults)
        self.index = data.get("index", "")
        self.name = data.get("name", "Unknown")
        self.image_url = data.get("full_image_url")
        
        # Validate and extract required fields (fail fast)
        self._validate_and_extract_required_fields()
        
        # Compute derived attributes once (cache for performance)
        self._compute_derived_attributes()
    
    def _validate_and_extract_required_fields(self) -> None:
        """Validate and extract required fields from API data.
        
        Raises:
            ValueError: If any required field is missing or invalid
        """
        # Hit points (required)
        if "hit_points" not in self._data:
            raise ValueError(f"Monster '{self.name}' missing required 'hit_points' data")
        self._hp = self._data["hit_points"]
        
        # Armor class (required)
        armor_class = self._data.get("armor_class", [])
        if not armor_class or len(armor_class) == 0:
            raise ValueError(f"Monster '{self.name}' missing required 'armor_class' data")
        ac_value = armor_class[0].get("value")
        if ac_value is None:
            raise ValueError(f"Monster '{self.name}' has invalid 'armor_class' structure")
        self._ac = ac_value
        
        # Strength (required)
        if "strength" not in self._data:
            raise ValueError(f"Monster '{self.name}' missing required 'strength' data")
        self._strength = self._data["strength"]
        
        # Optional fields with defaults
        self._proficiency_bonus = self._data.get("proficiency_bonus", 2)
        self._hit_dice = self._data.get("hit_dice", "1d8")
    
    def _compute_derived_attributes(self) -> None:
        """Compute derived attributes once during initialization.
        
        This avoids expensive recomputation on every property access.
        """
        # Parse hit dice to get die size
        self._hit_die_size = parse_hit_dice(self._hit_dice)
        
        # Calculate strength modifier
        self._str_modifier = self._get_modifier(self._strength)
        
        # Calculate attack bonus (STR modifier + proficiency)
        self._attack_bonus = self._str_modifier + self._proficiency_bonus
        
        # Build damage dice notation (1d{die_size} + STR_mod)
        if self._str_modifier >= 0:
            self._damage_dice = f"1d{self._hit_die_size}+{self._str_modifier}"
        else:
            self._damage_dice = f"1d{self._hit_die_size}{self._str_modifier}"
        
        # Store parsed damage dice components directly (avoid re-parsing)
        self._damage_dice_parsed = (1, self._hit_die_size, self._str_modifier)
    
    @staticmethod
    def _get_modifier(ability_score: int) -> int:
        """Calculate D&D ability modifier from ability score.
        
        Args:
            ability_score: The ability score value (e.g., Strength)
            
        Returns:
            The calculated modifier using D&D 5e formula: (score - 10) // 2
        """
        return (ability_score - 10) // 2
    
    # Properties - lightweight accessors returning cached values
    
    @property
    def hp(self) -> int:
        """Return the monster's hit points."""
        return self._hp
    
    @property
    def ac(self) -> int:
        """Return the monster's armor class (Defense)."""
        return self._ac
    
    @property
    def strength(self) -> int:
        """Return the monster's Strength score."""
        return self._strength
    
    @property
    def proficiency_bonus(self) -> int:
        """Return the monster's proficiency bonus."""
        return self._proficiency_bonus
    
    @property
    def hit_dice(self) -> str:
        """Return hit dice notation (e.g., '18d10')."""
        return self._hit_dice
    
    @property
    def hit_die_size(self) -> int:
        """Return the size of the hit die (e.g., 10 from '18d10')."""
        return self._hit_die_size
    
    @property
    def attack_bonus(self) -> int:
        """Return attack bonus: STR modifier + proficiency."""
        return self._attack_bonus
    
    @property
    def damage_dice(self) -> str:
        """Return damage dice notation: 1d{hit_die} + STR_mod."""
        return self._damage_dice
    
    @property
    def damage_dice_parsed(self) -> tuple[int, int, int]:
        """Return parsed damage as (num_dice, die_size, modifier)."""
        return self._damage_dice_parsed
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    def __repr__(self) -> str:
        return f"Monster(name='{self.name}', hp={self.hp}, ac={self.ac})"


