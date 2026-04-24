from pydantic import BaseModel, Field
from typing import Literal


class MushroomsSchema(BaseModel):
    cap_shape: Literal['b', 'c', 'x', 'f', 'k', 's'] = Field(..., alias='cap-shape')
    cap_surface: Literal['f', 'g', 'y', 's'] = Field(..., alias='cap-surface')
    cap_color: Literal['n', 'b', 'c', 'g', 'r', 'p', 'u', 'e', 'w', 'y'] = Field(..., alias='cap-color')
    bruises: Literal['t', 'f'] = Field(..., alias='bruises')
    odor: Literal['a', 'l', 'c', 'y', 'f', 'm', 'n', 'p', 's'] = Field(..., alias='odor')
    gill_attachment: Literal['a', 'd', 'f', 'n'] = Field(..., alias='gill-attachment')
    gill_spacing: Literal['c', 'w', 'd'] = Field(..., alias='gill-spacing')
    gill_size: Literal['b', 'n'] = Field(..., alias='gill-size')
    gill_color: Literal['k', 'n', 'b', 'h', 'g', 'r', 'o', 'p', 'u', 'e', 'w', 'y'] = Field(..., alias='gill-color')
    stalk_shape: Literal['e', 't'] = Field(..., alias='stalk-shape')
    stalk_root: Literal['b', 'c', 'u', 'e', 'z', 'r', '?'] = Field(..., alias='stalk-root')
    stalk_surface_above_ring: Literal['f', 'y', 'k', 's'] = Field(..., alias='stalk-surface-above-ring')
    stalk_surface_below_ring: Literal['f', 'y', 'k', 's'] = Field(..., alias='stalk-surface-below-ring')
    stalk_color_above_ring: Literal['n', 'b', 'c', 'g', 'o', 'p', 'e', 'w', 'y'] = Field(..., alias='stalk-color-above-ring')
    stalk_color_below_ring: Literal['n', 'b', 'c', 'g', 'o', 'p', 'e', 'w', 'y'] = Field(..., alias='stalk-color-below-ring')
    veil_type: Literal['p', 'u'] = Field(..., alias='veil-type')
    veil_color: Literal['n', 'o', 'w', 'y'] = Field(..., alias='veil-color')
    ring_number: Literal['n', 'o', 't'] = Field(..., alias='ring-number')
    ring_type: Literal['c', 'e', 'f', 'l', 'n', 'p', 's', 'z'] = Field(..., alias='ring-type')
    spore_print_color: Literal['k', 'n', 'b', 'h', 'r', 'o', 'u', 'w', 'y'] = Field(..., alias='spore-print-color')
    population: Literal['a', 'c', 'n', 's', 'v', 'y'] = Field(..., alias='population')
    habitat: Literal['g', 'l', 'm', 'p', 'u', 'w', 'd'] = Field(..., alias='habitat')

    class Config:
        populate_by_name = True
