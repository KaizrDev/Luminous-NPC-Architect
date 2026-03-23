---
description: Creates asset metadata files, directory plans, or full pipeline roadmaps for 2D/3D game assets.
---

# /luminous-asset

Creates organized metadata and pipeline plans for game assets.

## Steps

1. **Ask the user** for the following information if not already provided:
   - **Asset Type**: One of `sprite`, `spritesheet`, `3d-model`, `audio`, `tilemap`, or `directory-plan`.
   - **Asset Name**: The name of the asset (e.g., `player_run`, `forest_tileset`, `sword_swing_sfx`).
   - **Target Engine**: One of `unity`, `godot`, or `python`.
   - **Details** (optional): Additional context like dimensions, frame count, poly budget, etc.

2. **Generate the asset metadata** based on the type.

   ### For `sprite`:
   ```json
   {
     "asset_name": "player_idle",
     "type": "sprite",
     "format": "PNG",
     "dimensions": { "width": 64, "height": 64 },
     "pivot": { "x": 0.5, "y": 0.0 },
     "pixels_per_unit": 16,
     "tags": ["character", "player", "idle"],
     "notes": "Single-frame idle sprite. Transparent background."
   }
   ```

   ### For `spritesheet`:
   ```json
   {
     "asset_name": "player_run",
     "type": "spritesheet",
     "format": "PNG",
     "sheet_dimensions": { "width": 512, "height": 64 },
     "frame_size": { "width": 64, "height": 64 },
     "frame_count": 8,
     "fps": 12,
     "loop": true,
     "animations": [
       {
         "name": "run",
         "start_frame": 0,
         "end_frame": 7,
         "loop": true
       }
     ],
     "collision_box": { "offset_x": 8, "offset_y": 0, "width": 48, "height": 64 },
     "tags": ["character", "player", "movement"]
   }
   ```

   ### For `3d-model`:
   ```json
   {
     "asset_name": "fantasy_sword",
     "type": "3d_model",
     "format": "GLTF",
     "poly_budget": 5000,
     "texture_resolution": 1024,
     "lod_levels": [
       { "level": 0, "max_polys": 5000, "distance": 0 },
       { "level": 1, "max_polys": 2500, "distance": 20 },
       { "level": 2, "max_polys": 800, "distance": 50 }
     ],
     "materials": ["blade_metal", "handle_leather", "gem_emissive"],
     "rigged": false,
     "tags": ["weapon", "melee", "fantasy"]
   }
   ```

   ### For `audio`:
   ```json
   {
     "asset_name": "sword_swing",
     "type": "audio",
     "category": "sfx",
     "format": "OGG",
     "duration_seconds": 0.5,
     "sample_rate": 44100,
     "channels": "mono",
     "volume_db": -6,
     "loop": false,
     "tags": ["combat", "weapon", "swing"]
   }
   ```

   ### For `tilemap`:
   ```json
   {
     "asset_name": "forest_tileset",
     "type": "tilemap",
     "format": "PNG",
     "tile_size": { "width": 16, "height": 16 },
     "tileset_dimensions": { "columns": 8, "rows": 8, "total_tiles": 64 },
     "terrain_types": ["grass", "dirt", "water", "stone", "tree_base"],
     "auto_tile": true,
     "collision_tiles": [12, 13, 14, 48, 49, 50],
     "tags": ["environment", "outdoor", "forest"]
   }
   ```

   ### For `directory-plan`:
   Generate a full asset directory organizational plan:
   ```
   assets/
   ├── textures/
   │   ├── characters/
   │   │   ├── player/
   │   │   └── npcs/
   │   ├── environment/
   │   │   ├── tilesets/
   │   │   └── props/
   │   ├── ui/
   │   │   ├── icons/
   │   │   ├── buttons/
   │   │   └── backgrounds/
   │   └── fx/
   ├── audio/
   │   ├── sfx/
   │   │   ├── combat/
   │   │   ├── ui/
   │   │   └── environment/
   │   └── music/
   │       ├── gameplay/
   │       └── menus/
   ├── models/         (3D projects only)
   │   ├── characters/
   │   ├── props/
   │   └── environment/
   ├── animations/
   │   ├── characters/
   │   └── fx/
   └── fonts/
   ```

3. **Save the metadata file**:
   - For individual assets: `assets/<category>/<asset_name>.meta.json`
   - For directory plans: `docs/asset_pipeline.md`

4. **If type is `3d-model`**, also generate a **pipeline roadmap**:
   ```markdown
   # 3D Asset Pipeline: <asset_name>

   ## Phase 1: Modeling (Days 1-5)
   - Block out base shape in Blender
   - Refine silhouette within poly budget (<poly_budget> tris)
   - Create LOD variants

   ## Phase 2: UV & Texturing (Days 6-10)
   - Unwrap UVs with minimal distortion
   - Bake normal and AO maps
   - Paint textures at <texture_resolution>px

   ## Phase 3: Rigging & Animation (Days 11-15)
   - (If rigged) Create skeleton and weight paint
   - Create animation clips

   ## Phase 4: Export & Integration (Days 16-18)
   - Export as GLTF/FBX
   - Import into engine, verify materials
   - Set up LOD switching
   - Performance test
   ```

5. **Report the result** to the user, including:
   - The generated metadata content.
   - File location.
   - Any recommendations (e.g., "Consider adding LOD levels for models over 3000 polys.").
