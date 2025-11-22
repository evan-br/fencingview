"""
Quick demo script for FencingView analysis.

Usage:
    python examples/demo_analysis.py                    # Use default video "epee1.mp4"
    python examples/demo_analysis.py path/to/video.mp4 # Use custom video file

Press 'q' in preview window to exit early.
"""

import sys
import os
import argparse

# Add src directory to path for development
sys.path.insert(0, os.path.abspath("src"))

from fencingview import EpeeMatch


def main():
    """Run FencingView analysis on a video file."""
    
    parser = argparse.ArgumentParser(
        description="Analyze epee fencing video with FencingView",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python examples/demo_analysis.py                        # Analyze epee1.mp4 (default)
  python examples/demo_analysis.py path/to/match.mp4      # Analyze custom video
  python examples/demo_analysis.py --no-preview video.mp4 # Analysis without preview
        """
    )
    
    parser.add_argument(
        "video",
        nargs="?",
        default="epee1.mp4",
        help="Path to video file (default: epee1.mp4)"
    )
    
    parser.add_argument(
        "--no-preview",
        action="store_true",
        help="Disable preview window (faster)"
    )
    
    args = parser.parse_args()
    
    # Validate video file exists
    if not os.path.exists(args.video):
        print(f"❌ Error: Video file not found: {args.video}")
        print("\nPlease provide a valid video path:")
        print(f"  python examples/demo_analysis.py {args.video}")
        sys.exit(1)
    
    # Run analysis
    try:
        print(f"🎬 Loading video: {args.video}")
        match = EpeeMatch(args.video)
        
        print("🔬 Starting analysis...")
        show_preview = not args.no_preview
        
        frame_count = 0
        players_detected = 0
        
        for frame_data in match.analyze(show_preview=show_preview):
            frame_count += 1
            
            # Log progress every 30 frames
            if frame_count % 30 == 0:
                print(f"  ✓ Frame {frame_data['frame_id']} processed")
            
            # Count frames with both players detected
            if "A" in frame_data["players"] and "B" in frame_data["players"]:
                players_detected += 1
                
                # Print sample output for first few detections
                if frame_count <= 3 or frame_count % 150 == 0:
                    player_a = frame_data["players"]["A"]
                    player_b = frame_data["players"]["B"]
                    print(f"\n  Frame {frame_data['frame_id']} Sample:")
                    print(f"    Player A: {player_a['action']} | {player_a['movement']}")
                    print(f"    Player B: {player_b['action']} | {player_b['movement']}")
        
        # Summary
        print(f"\n{'='*50}")
        print(f"✅ Analysis Complete!")
        print(f"   Total frames processed: {frame_count}")
        print(f"   Frames with 2 players: {players_detected}")
        if frame_count > 0:
            print(f"   Detection rate: {100*players_detected/frame_count:.1f}%")
        print(f"{'='*50}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Analysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
