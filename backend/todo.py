def assign_prompts(assigned_roles, story_type):
    assigned_prompts = {}
    for player, role in assigned_roles.items():
        role_prompts = prompts.get(story_type, {}).get(role, [])
        if role_prompts:
            selected_prompt = random.choice(role_prompts)
            assigned_prompts[player] = selected_prompt
    return assigned_prompts

def distribute_prompts(lobby_code):
    if lobby_code in lobbies:
        players = lobbies[lobby_code]['players']
        category = lobbies[lobby_code]['category']
        role_assignments = lobbies[lobby_code]['roles']  # Assuming you've stored roles here
        
        player_prompts = {}
        
        for player, role in role_assignments.items():
            available_prompts = prompts[category][role]
            selected_prompts = random.sample(available_prompts, min(3, len(available_prompts)))  # Select up to 3 prompts
            player_prompts[player] = selected_prompts
            
        lobbies[lobby_code]['prompts'] = player_prompts  # Store the prompts for later use
        
        return player_prompts
    else:
        return "Lobby not found", 404
    
def compile_script(lobby_code):
    if lobby_code not in lobbies:
        return "Lobby not found", 404
    
    # Retrieve stored prompts and player responses
    player_prompts = lobbies[lobby_code]['prompts']
    player_responses = lobbies[lobby_code]['responses']  # Assuming you've stored player responses here
    
    # Initialize script segments
    intro = []
    middle = []
    end = []
    
    # Organize responses into script segments
    for player, prompts in player_prompts.items():
        for prompt in prompts:
            part = prompt['part']
            role = prompt['role']
            context = prompt['context']
            
            response = player_responses.get(player, {}).get(prompt['id'], "")
            
            filled_context = context.format(response=response)
            
            if part == "introduction":
                intro.append(filled_context)
            elif part == "middle":
                middle.append(filled_context)
            elif part == "end":
                end.append(filled_context)
                
    # Compile the final script
    final_script = "\n".join(intro + middle + end)
    
    return final_script
