/**
 * Плагин jarvis-switch — добавляет команды «Визуал» и «Чат» в ⌘K-палитру Hermes.
 */
import { PALETTE_AREA } from '@hermes/plugin-sdk';

const SCRIPT_VISUAL = 'C:/Users/Пользователь/Desktop/Для Джарвиса/1_ВИЗУАЛ.vbs';
const SCRIPT_CHAT = 'C:/Users/Пользователь/Desktop/Для Джарвиса/2_ЧАТ.vbs';

function register(ctx) {
  ctx.register({
    id: 'jarvis-visual',
    area: PALETTE_AREA,
    data: {
      id: 'jarvis.switchVisual',
      label: 'Jarvis: Визуал',
      keywords: ['jarvis', 'визуал', 'visual', 'hud', 'переключить'],
      run: () => {
        ctx.os.openExternal(SCRIPT_VISUAL);
      },
    },
  });

  ctx.register({
    id: 'jarvis-chat',
    area: PALETTE_AREA,
    data: {
      id: 'jarvis.switchChat',
      label: 'Jarvis: Чат',
      keywords: ['jarvis', 'чат', 'chat', 'hermes', 'переключить'],
      run: () => {
        ctx.os.openExternal(SCRIPT_CHAT);
      },
    },
  });
}

export default {
  id: 'jarvis-switch',
  name: 'Jarvis Switch',
  defaultEnabled: false,
  register,
};