﻿using Axiro.Services;
using Discord.Interactions;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Axiro.Modules
{
    public class MiscCommands : InteractionModuleBase<SocketInteractionContext>
    {
        public InteractionService Commands { get; set; }

        private CommandHandler _handler;

        public MiscCommands(CommandHandler handler)
        {
            _handler = handler;
        }
    }
}
