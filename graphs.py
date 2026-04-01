import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from collections import Counter
import random

def load_json_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_creator_colors(badges):
    unique_creators = {}
    colors = [
        '#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00',
        '#ffff33', '#a65628', '#f781bf', '#999999', '#66c2a5',
        '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f',
        '#e5c494', '#b3b3b3', '#1b9e77', '#d95f02', '#7570b3'
    ]
    for badge in badges:
        creator_id = badge['creatorId']
        if creator_id not in unique_creators:
            unique_creators[creator_id] = {
                'name': badge['creatorName'],
                'color': colors[len(unique_creators) % len(colors)]
            }
    return unique_creators

def format_rank(rank):
    if rank == 255:
        return "Owner"
    elif 200 < rank < 255:
        return str(rank)
    return None

def get_user_groups_by_rank(groups):
    high_rank_groups = []
    for group in groups:
        rank = group['rank']
        formatted = format_rank(rank)
        if formatted:
            high_rank_groups.append({
                'name': group['groupName'],
                'rank': formatted,
                'role': group['roleName']
            })
    return sorted(high_rank_groups, key=lambda x: int(x['rank']) if x['rank'] != "Owner" else 255, reverse=True)

def process_badges_by_date(badges):
    date_counts = Counter()
    date_creators = {}
    
    for badge in badges:
        if not badge.get('awardedDate'):
            continue
        try:
            date_str = badge['awardedDate'][:10]
            date_counts[date_str] += 1
            
            if date_str not in date_creators:
                date_creators[date_str] = []
            date_creators[date_str].append(badge['creatorId'])
        except:
            continue
    
    return date_counts, date_creators

def process_badges_by_id(badges):
    id_counts = Counter()
    badge_ids = []
    
    for badge in badges:
        bid = badge.get('id')
        if bid:
            badge_ids.append((bid, badge.get('creatorId')))
    
    badge_ids.sort(key=lambda x: x[0])
    
    return badge_ids

def create_visualization(json_file, output_file='badge_timeline.png'):
    data = load_json_data(json_file)
    
    badges = data.get('badges', [])
    groups = data.get('groups', [])
    username = data.get('username', 'Unknown')
    
    creator_colors = get_creator_colors(badges)
    date_counts, date_creators = process_badges_by_date(badges)
    
    has_dates = bool(date_counts)
    
    if not has_dates:
        badge_ids = process_badges_by_id(badges)
        if not badge_ids:
            print("No badge data found.")
            return
        id_counts = Counter()
        for bid, _ in badge_ids:
            bucket = (bid // 5000) * 5000
            id_counts[bucket] += 1
        
        sorted_ids = sorted(id_counts.keys())
        counts = [id_counts[k] for k in sorted_ids]
        
        high_rank_groups = get_user_groups_by_rank(groups)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12), gridspec_kw={'height_ratios': [3, 1]})
        fig.suptitle(f'Badge Timeline for {username} (by Badge ID - no awardedDate)', fontsize=16, fontweight='bold')
        
        bars = ax1.bar(range(len(sorted_ids)), counts, width=0.8, color='#4daf4a', edgecolor='#2d7d4f', alpha=0.8)
        
        for bar, count in zip(bars, counts):
            ax1.annotate(f'{count}',
                        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax1.set_xlabel('Badge ID Range (approximate timeline)', fontsize=12)
        ax1.set_ylabel('Number of Badges', fontsize=12)
        ax1.set_title('Badges by ID Range (higher ID = newer)', fontsize=12)
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        ax1.set_axisbelow(True)
        
        ax1.set_xticks(range(len(sorted_ids)))
        ax1.set_xticklabels([f"{k:,}" for k in sorted_ids], rotation=45, ha='right', fontsize=8)
        
        legend_text = "Top Badge Creators:\n"
        for cid, info in list(creator_colors.items())[:10]:
            legend_text += f"■ {info['name'][:25]}\n"
        ax1.text(0.02, 0.98, legend_text, transform=ax1.transAxes, fontsize=8,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
        
        ax2.set_title(f'User Groups with Rank > 200 ({len(high_rank_groups)} groups)', fontsize=11)
        ax2.axis('off')
        
        if high_rank_groups:
            group_info = "Rank | Group Name\n" + "-" * 40 + "\n"
            for g in high_rank_groups[:15]:
                rank_str = f"[{g['rank']}]"
                group_info += f"{rank_str:>6} | {g['name'][:30]}\n"
            if len(high_rank_groups) > 15:
                group_info += f"\n... and {len(high_rank_groups) - 15} more"
            ax2.text(0.02, 0.95, group_info, transform=ax2.transAxes, fontsize=9,
                     verticalalignment='top', fontfamily='monospace',
                     bbox=dict(boxstyle='round', facecolor='#f0f0f0', alpha=0.9))
        else:
            ax2.text(0.02, 0.95, "No groups with rank > 200 found", transform=ax2.transAxes, fontsize=10,
                     verticalalignment='top', bbox=dict(boxstyle='round', facecolor='#f0f0f0', alpha=0.9))
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Visualization saved to {output_file}")
        
        print(f"\n=== Summary ===")
        print(f"Note: No awardedDate in JSON, using badge ID as timeline proxy")
        print(f"Total badges: {len(badges)}")
        print(f"Unique creators: {len(creator_colors)}")
        print(f"ID ranges: {len(id_counts)}")
        print(f"Groups with rank > 200: {len(high_rank_groups)}")
        return
    
    sorted_dates = sorted(date_counts.keys())
    counts = [date_counts[d] for d in sorted_dates]
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in sorted_dates]
    
    high_rank_groups = get_user_groups_by_rank(groups)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12), gridspec_kw={'height_ratios': [3, 1]})
    fig.suptitle(f'Badge Timeline for {username}', fontsize=16, fontweight='bold')
    
    bars = ax1.bar(dates, counts, width=0.8, color='#4daf4a', edgecolor='#2d7d4f', alpha=0.8)
    
    for i, (bar, date_str) in enumerate(zip(bars, sorted_dates)):
        height = bar.get_height()
        ax1.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Number of Badges', fontsize=12)
    ax1.set_title('Badges Awarded Per Day', fontsize=12)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_axisbelow(True)
    
    legend_text = "Top Badge Creators:\n"
    for cid, info in list(creator_colors.items())[:10]:
        legend_text += f"■ {info['name'][:25]}\n"
    ax1.text(0.02, 0.98, legend_text, transform=ax1.transAxes, fontsize=8,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    ax2.set_title(f'User Groups with Rank > 200 ({len(high_rank_groups)} groups)', fontsize=11)
    ax2.axis('off')
    
    if high_rank_groups:
        group_info = "Rank | Group Name\n" + "-" * 40 + "\n"
        for g in high_rank_groups[:15]:
            rank_str = f"[{g['rank']}]"
            group_info += f"{rank_str:>6} | {g['name'][:30]}\n"
        if len(high_rank_groups) > 15:
            group_info += f"\n... and {len(high_rank_groups) - 15} more"
        ax2.text(0.02, 0.95, group_info, transform=ax2.transAxes, fontsize=9,
                 verticalalignment='top', fontfamily='monospace',
                 bbox=dict(boxstyle='round', facecolor='#f0f0f0', alpha=0.9))
    else:
        ax2.text(0.02, 0.95, "No groups with rank > 200 found", transform=ax2.transAxes, fontsize=10,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='#f0f0f0', alpha=0.9))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Visualization saved to {output_file}")
    
    print(f"\n=== Summary ===")
    print(f"Total badges: {len(badges)}")
    print(f"Unique creators: {len(creator_colors)}")
    print(f"Days with badges: {len(date_counts)}")
    print(f"Groups with rank > 200: {len(high_rank_groups)}")

if __name__ == '__main__':
    import sys
    json_file = sys.argv[1] if len(sys.argv) > 1 else 'NattJuh.json'
    output_file = json_file.replace('.json', '_badges_timeline.png')
    create_visualization(json_file, output_file)
