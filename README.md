# Discogs Collection Workflow

An intelligent music recommendation system powered by [crewAI](https://crewai.com) that analyzes your Discogs collection, generates personalized song suggestions, and automatically organizes them into curated folders on Discogs.

## Overview

This workflow uses AI agents to analyze your Discogs music collection, generate personalized recommendations based on your listening preferences, search the Discogs database for available releases, and automatically create organized folders in your collection with curated suggestions and popular picks.

### What It Does

The workflow executes a sequential pipeline that:

1. **Analyzes your Discogs collection** - Retrieves all releases from your personal collection with complete metadata
2. **Generates personalized recommendations** - Creates 10 song suggestions based on patterns in your collection (genres, artists, styles)
3. **Searches for available releases** - Finds exact or close matches for each suggestion in the Discogs database
4. **Creates a "Suggested" folder** - Automatically adds all matched releases to a timestamped `CrewSuggested_[timestamp]` folder in your collection
5. **Ranks by popularity** - Analyzes community metrics (wants/haves counts) to identify the top 3 most popular releases
6. **Creates a "Popular" folder** - Adds the top 3 releases to a timestamped `CrewPopular_[timestamp]` folder in your collection

### Artifacts Created

The workflow creates two folders in your Discogs collection:

- **`CrewSuggested_[timestamp]`** - Contains all successfully matched song recommendations from the search (typically up to 10 releases)
- **`CrewPopular_[timestamp]`** - Contains the top 3 most popular releases based on Discogs community engagement metrics

## Architecture

### AI Agents

The workflow is powered by three specialized AI agents:

1. **Song Recommender** (`song_recommender`)
   - Role: Music Recommendation Specialist
   - Analyzes collection patterns (artists, genres, styles, years)
   - Generates diverse, personalized song suggestions
   - Ensures variety across artists and genres

2. **Popularity Picker** (`popularity_picker`)
   - Role: Music Popularity Analyst
   - Evaluates releases using Discogs community metrics
   - Calculates popularity scores from wants/haves counts
   - Ranks and selects top releases with detailed reasoning

3. **Discogs API Agent** (`discogs_api_agent`)
   - Role: Discogs API Integration Specialist
   - Executes all Discogs API operations via MCP server
   - Handles collection retrieval, database searches, folder creation
   - Manages pagination and error handling

### Task Pipeline

Six sequential tasks orchestrate the workflow:

1. **`get_collection_task`** - Retrieves complete collection with pagination
2. **`generate_suggestions_task`** - Creates 10 personalized recommendations
3. **`search_and_filter_releases_task`** - Searches Discogs and filters results
4. **`create_suggested_folder_task`** - Creates folder and adds all matches
5. **`select_top_popular_task`** - Ranks releases by popularity metrics
6. **`create_popular_folder_task`** - Creates folder and adds top 3 releases

### Technology Stack

- **crewAI 1.9.3** - Multi-agent orchestration framework with tools support
- **MCP (Model Context Protocol)** - Standardized interface for Discogs API integration
- **MusicAgent MCP Server** - Custom MCP server exposing Discogs API tools
- **AI Models** - Supports Anthropic Claude or OpenAI GPT models
- **Python 3.11-3.13** - Runtime environment
- **UV Package Manager** - Dependency management and project setup

### MCP Integration

The workflow integrates with the Discogs API through a custom MCP server:

- **MCP Server Location**: `../MusicAgent/mcp_server.py`
- **Wrapper Script**: `../discogs_mcp.py` (ultra-short path for tool name compatibility)
- **Available MCP Tools**:
  - `get_collection_releases` - Retrieve user's collection with pagination
  - `add_release_to_collection` - Add release to collection folder
  - `create_collection_folder` - Create new collection folder
  - `search_by_artist` - Search database by artist name
  - `search_by_title` - Search database by title
  - `search_by_genre` - Search database by genre
  - `search_by_artist_and_title` - Search by both artist and title

The MCP server provides a standardized interface between the AI agents and the Discogs API, handling authentication, rate limiting, and data formatting automatically.

For more information and source code, please check out: https://github.com/sallocc/MusicAgent

## Installation

### Prerequisites

- Python >=3.11, <3.14
- [UV package manager](https://docs.astral.sh/uv/) (recommended)
- Discogs account with API token
- Anthropic or OpenAI API key

### Setup Steps

1. **Install UV** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Navigate to the project directory**:
   ```bash
   cd discogsworkflow
   ```

3. **Install dependencies**:
   ```bash
   crewai install
   ```
   
   Or manually with UV:
   ```bash
   uv sync
   ```

4. **Configure environment variables** (`.env` file):
   
   Create a `.env` file in the `discogsworkflow` directory with the following:

   ```bash
   # AI Model API Key (choose one)
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   # OR
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Discogs API Configuration
   DISCOGS_API_TOKEN=your_discogs_token_here
   DISCOGS_USER_AGENT=YourAppName/1.0 +https://yourwebsite.com
   
   # Optional: Specify model (default: gpt-4o)
   MODEL=gpt-4o
   # Or use Claude:
   # MODEL=claude-3-5-sonnet-20241022
   ```

   **How to get credentials:**
   
   - **Discogs API Token**: Visit [Discogs Developer Settings](https://www.discogs.com/settings/developers) and generate a personal access token
   - **Anthropic API Key**: Sign up at [Anthropic Console](https://console.anthropic.com/)
   - **OpenAI API Key**: Sign up at [OpenAI Platform](https://platform.openai.com/)

5. **Set up MCP Server Dependencies**:
   
   The workflow requires the MusicAgent MCP server to be available. Ensure the `../MusicAgent` directory exists with:
   - `mcp_server.py` - The MCP server implementation
   - `.env` file with `DISCOGS_API_TOKEN` and `DISCOGS_USER_AGENT`
   - Required dependencies installed

   To set up the MusicAgent MCP server:
   ```bash
   cd ../MusicAgent
   pip install -r requirements.txt
   ```

6. **Update username** (optional):
   
   By default, the workflow uses the username `simonallocca6`. To use your own Discogs username, edit [`src/discogsworkflow/main.py`](src/discogsworkflow/main.py):
   
   ```python
   inputs = {
       'username': 'your_discogs_username'
   }
   ```

## Running the Workflow

### Standard Execution

From the `discogsworkflow` directory, run:

```bash
crewai run
```

Or:

```bash
uv run discogsworkflow
```

### Expected Output

The workflow will display progress for each task:

```
============================================================
🎵 Starting Discogs Collection Workflow
============================================================

Username: your_username

This workflow will:
  1. Analyze your Discogs collection
  2. Generate 10 personalized song suggestions
  3. Search for available releases on Discogs
  4. Create a 'CrewSuggested' folder with all matches
  5. Identify the top 3 most popular releases
  6. Create a 'CrewPopular' folder with the top picks

============================================================

[Agent execution logs...]

============================================================
✅ Discogs Workflow Completed Successfully!
============================================================

Check your Discogs collection for the new folders:
  • CrewSuggested_[timestamp]
  • CrewPopular_[timestamp]

============================================================
```

### Viewing Results

After completion, visit your [Discogs collection](https://www.discogs.com/user/your_username/collection) to see the newly created folders with curated recommendations.

## Customization

### Modifying Agents

Edit [`src/discogsworkflow/config/agents.yaml`](src/discogsworkflow/config/agents.yaml) to customize agent behaviors:

```yaml
song_recommender:
  role: >
    Music Recommendation Specialist
  goal: >
    Your custom goal here
  backstory: >
    Your custom backstory here
```

### Modifying Tasks

Edit [`src/discogsworkflow/config/tasks.yaml`](src/discogsworkflow/config/tasks.yaml) to adjust task descriptions and expected outputs:

```yaml
generate_suggestions_task:
  description: >
    Your custom task description
  expected_output: >
    Your custom expected output format
  agent: song_recommender
```

### Advanced Configuration

- **Change AI model**: Update `MODEL` in `.env` (e.g., `claude-3-5-sonnet-20241022`, `gpt-4o`, `gpt-4-turbo`)
- **Adjust suggestion count**: Modify the task descriptions in `tasks.yaml` to generate more/fewer suggestions
- **Add custom tools**: Extend [`src/discogsworkflow/tools/custom_tool.py`](src/discogsworkflow/tools/custom_tool.py)
- **Modify process type**: Change `Process.sequential` to `Process.hierarchical` in [`crew.py`](src/discogsworkflow/crew.py)

## Troubleshooting

### Common Issues

1. **MCP Server not found**
   - Ensure `../discogs_mcp.py` and `../MusicAgent/mcp_server.py` exist
   - Verify the MusicAgent dependencies are installed

2. **Authentication errors**
   - Verify your `DISCOGS_API_TOKEN` is valid and not expired
   - Check that the token is set in both `.env` files (discogsworkflow and MusicAgent)

3. **Rate limiting**
   - Discogs API allows 60 requests/minute for authenticated users
   - The MCP server handles rate limiting automatically
   - If you hit limits, the workflow will pause and retry

4. **No matches found**
   - Some song suggestions may not be available on Discogs
   - The workflow gracefully handles missing releases and continues with available matches

5. **API key errors**
   - Ensure you have either `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` set
   - Check for typos or invalid keys
   - Verify your API account has available credits

## Development

### Project Structure

```
discogsworkflow/
├── src/discogsworkflow/
│   ├── config/
│   │   ├── agents.yaml          # Agent configurations
│   │   └── tasks.yaml           # Task definitions
│   ├── tools/
│   │   └── custom_tool.py       # Custom tool implementations
│   ├── crew.py                  # Crew and agent definitions
│   └── main.py                  # Entry point
├── knowledge/                    # Knowledge sources (optional)
├── logs/                         # Execution logs
├── exports/                      # Export directory
├── .env                         # Environment configuration
├── pyproject.toml               # Project dependencies
└── README.md                    # This file
```

### Training and Testing

Train the crew for improved performance:

```bash
crewai train --n_iterations 5 --filename training_data.pkl
```

Test the crew:

```bash
crewai test --n_iterations 3 --eval_llm gpt-4o
```

Replay a specific task:

```bash
crewai replay <task_id>
```

## Implementation Notes

### MCP Server Path Optimization

The workflow uses an ultra-short wrapper script (`discogs_mcp.py`) to launch the MCP server. This is necessary because crewAI has a 64-character limit on tool names, and long file paths can cause tool name truncation issues. The wrapper ensures maximum compatibility while maintaining clean tool naming.

### Sequential Processing

The workflow uses sequential processing to ensure each task completes before the next begins. This is critical for maintaining data dependencies (e.g., collection analysis must complete before generating suggestions).

### Error Handling

The Discogs API agent includes robust error handling for:
- API rate limits and retries
- Missing releases in search results
- Folder creation failures
- Network connectivity issues

## Support and Resources

- **crewAI Documentation**: [https://docs.crewai.com](https://docs.crewai.com)
- **Discogs API Documentation**: [https://www.discogs.com/developers](https://www.discogs.com/developers)
- **crewAI GitHub**: [https://github.com/joaomdmoura/crewai](https://github.com/joaomdmoura/crewai)
- **MCP Protocol**: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)

## License

This project is part of the MusicAgent ecosystem. See the LICENSE file for details.

---

Built with ❤️ using crewAI and the Model Context Protocol
