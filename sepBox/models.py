from django.db import models

class VerticalSeparatorDesign(models.Model):
    # --- Input Parameters ---
    name = models.CharField(max_length=100, help_text="Design case identifier")

    # Flow properties
    Wg = models.FloatField(help_text="Gas mass flow rate (lb/hr)")
    Wl = models.FloatField(help_text="Liquid mass flow rate (lb/hr)")
    Pg = models.FloatField(help_text="Gas density (lb/ft³)")
    Pl = models.FloatField(help_text="Liquid density (lb/ft³)")
    Ug = models.FloatField(help_text="Gas viscosity (cP)")
    dp = models.FloatField(help_text="Droplet diameter (ft)")

    # Design factors
    velocity_factor = models.FloatField(default=0.75, help_text="Velocity safety factor (typically 0.5 - 1.0)")
    holdup_time = models.IntegerField(default=5, help_text="Holdup time (minutes)")
    surge_factor = models.FloatField(default=1.5, help_text="Surge volume multiplier")
    pressure = models.FloatField(help_text="Operating pressure (psia)")
    mist_eliminator_ring = models.FloatField(default=0.5, help_text="Mist eliminator allowance (ft)")

    # New Input Fields
    dn = models.FloatField(help_text="Inlet nozzle diameter (ft)", null=True, blank=True)
    inlet_diverter = models.BooleanField(default=False, help_text="Is an inlet diverter present?")
    mist_eliminator_present = models.BooleanField(default=False, help_text="Is a mist eliminator installed?")

    # --- Computed Results ---
    Qg = models.FloatField(null=True, blank=True, help_text="Gas volumetric flow rate (ft³/min)")
    Ql = models.FloatField(null=True, blank=True, help_text="Liquid volumetric flow rate (ft³/min)")
    Cd = models.FloatField(null=True, blank=True, help_text="Drag coefficient (dimensionless)")
    K = models.FloatField(null=True, blank=True, help_text="Souders-Brown K value (ft/s)")
    Vt = models.FloatField(null=True, blank=True, help_text="Terminal velocity (ft/s)")
    Vv = models.FloatField(null=True, blank=True, help_text="Design gas velocity (ft/s)")
    Di = models.FloatField(null=True, blank=True, help_text="Internal vessel diameter (ft)")
    A = models.FloatField(null=True, blank=True, help_text="Cross-sectional area (ft²)")
    V_holdup = models.FloatField(null=True, blank=True, help_text="Holdup volume (ft³)")
    V_surge = models.FloatField(null=True, blank=True, help_text="Surge volume (ft³)")
    Holdup_Height = models.FloatField(null=True, blank=True, help_text="Height of holdup section (ft)")
    Surge_Height = models.FloatField(null=True, blank=True, help_text="Height of surge section (ft)")
    LLL = models.FloatField(null=True, blank=True, help_text="Low Liquid Level Height (inches)")
    Hd = models.FloatField(null=True, blank=True, help_text="Disengagement height (ft)")
    Hme = models.FloatField(null=True, blank=True, help_text="Mist eliminator height (ft)")
    H_total = models.FloatField(null=True, blank=True, help_text="Total separator height (ft)")
    H_lin = models.FloatField(null=True, blank=True, help_text="Height from liquid interface to nozzle centerline (ft)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Design: {self.name}"
class HorizontalSeparatorDesign(models.Model):
    # --- Input Parameters ---
    name = models.CharField(max_length=100, help_text="Design case identifier")

    # Flow properties
    Wg = models.FloatField(help_text="Gas mass flow rate (lb/hr)")
    Wl = models.FloatField(help_text="Liquid mass flow rate (lb/hr)")
    Pg = models.FloatField(help_text="Gas density (lb/ft³)")
    Pl = models.FloatField(help_text="Liquid density (lb/ft³)")
    Ug = models.FloatField(help_text="Gas viscosity (cP)")
    dp = models.FloatField(help_text="Droplet diameter (ft)")

    # Design factors
    velocity_factor = models.FloatField(default=0.75, help_text="Velocity safety factor (typically 0.5 - 1.0)")
    holdup_time = models.IntegerField(default=5, help_text="Holdup time (minutes)")
    surge_factor = models.FloatField(default=1.5, help_text="Surge volume multiplier")
    pressure = models.FloatField(help_text="Operating pressure (psia)")
    mist_eliminator_ring = models.FloatField(default=0.5, help_text="Mist eliminator allowance (ft)")
    L_D_ratio = models.FloatField(default=3.0, help_text="Length-to-diameter ratio")

    # Optional input flags
    mist_eliminator_present = models.BooleanField(default=False, help_text="Is a mist eliminator installed?")

    # --- Computed Results ---
    Qg = models.FloatField(null=True, blank=True)
    Ql = models.FloatField(null=True, blank=True)
    Cd = models.FloatField(null=True, blank=True)
    K = models.FloatField(null=True, blank=True)
    Vt = models.FloatField(null=True, blank=True)
    Vv = models.FloatField(null=True, blank=True)
    Di = models.FloatField(null=True, blank=True)
    A = models.FloatField(null=True, blank=True)
    L = models.FloatField(null=True, blank=True)
    V_holdup = models.FloatField(null=True, blank=True)
    V_surge = models.FloatField(null=True, blank=True)
    LLL = models.FloatField(null=True, blank=True)

    Holdup_Height = models.FloatField(null=True, blank=True, help_text="Height of holdup section (ft)")
    Surge_Height = models.FloatField(null=True, blank=True, help_text="Height of surge section (ft)")
    H_liquid = models.FloatField(null=True, blank=True, help_text="Total liquid height (ft)")
    Hme = models.FloatField(null=True, blank=True, help_text="Mist eliminator height (ft)")
    H_total = models.FloatField(null=True, blank=True, help_text="Total separator height (ft)")

    # Geometry variables
    D = models.FloatField(null=True, blank=True, help_text="Vessel internal diameter (ft)")
    Av = models.FloatField(null=True, blank=True, help_text="Gas area above liquid (ft²)")
    Hv = models.FloatField(null=True, blank=True, help_text="Height of vapor space above liquid (ft)")
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Horizontal Separator: {self.name}"
